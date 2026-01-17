"""Config flow for Fox Energy integration."""

import asyncio
import ipaddress
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_TIMEOUT
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from .api import FoxEnergyAPI, FoxEnergyConnectionError, FoxEnergyInvalidResponse
from .const import DOMAIN, DEFAULT_TIMEOUT, DEFAULT_SCAN_INTERVAL, CONF_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_NAME): str,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
    }
)


async def validate_host(hass: HomeAssistant, host: str) -> bool:
    """Validate that we can connect to the device.

    Args:
        hass: Home Assistant instance
        host: Device IP address

    Returns:
        True if connection successful, False otherwise
    """
    api = FoxEnergyAPI(host, DEFAULT_TIMEOUT)
    try:
        await api.detect_device_type()
        return True
    except (FoxEnergyConnectionError, FoxEnergyInvalidResponse) as err:
        _LOGGER.error("Connection error to %s: %s", host, err)
        return False


async def scan_network_for_devices(
    hass: HomeAssistant, subnet: str = None
) -> list[str]:
    """Scan network for Fox Energy devices.

    Args:
        hass: Home Assistant instance
        subnet: Network subnet to scan (e.g., "192.168.1")

    Returns:
        List of discovered device IPs
    """
    found_devices = []

    # If subnet not specified, try to detect from Home Assistant's network
    if subnet is None:
        # Try to get network info from HA - fallback to common private subnets
        # This scans the most common home network ranges
        try:
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            # Extract subnet from local IP (e.g., "192.168.1.50" -> "192.168.1")
            subnet = ".".join(local_ip.split(".")[:-1])
        except Exception:
            # Cannot detect network, return empty - user must enter IP manually
            return found_devices

    # Scan addresses in subnet
    base_parts = subnet.rsplit(".", 1)
    if len(base_parts) == 2:
        base = base_parts[0]
        # Scan range 1-254
        scan_range = range(1, 255)
    else:
        return found_devices

    # Create tasks for scanning (limit concurrency)
    tasks = []
    semaphore = asyncio.Semaphore(10)

    async def check_device(ip: str) -> str | None:
        async with semaphore:
            try:
                api = FoxEnergyAPI(ip, timeout=1)
                await asyncio.wait_for(
                    api.detect_device_type(),
                    timeout=1,
                )
                return ip
            except Exception:
                return None

    # Prepare all IP addresses to check
    for i in scan_range:
        ip = f"{base}.{i}"
        tasks.append(check_device(ip))

    # Run all checks concurrently
    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=False)
        found_devices = [ip for ip in results if ip is not None]

    return found_devices


class FoxEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Fox Energy integration."""

    VERSION = 1
    discovered_devices: list[str] = []

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create options flow."""
        return FoxEnergyOptionsFlow(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle user step - manual IP entry.

        Args:
            user_input: User input from form

        Returns:
            Flow result
        """
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate host
            host = user_input[CONF_HOST].strip()

            # Try to parse as IP
            try:
                ipaddress.ip_address(host)
            except ValueError:
                errors[CONF_HOST] = "invalid_host"

            if not errors:
                # Check if already configured
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()

                # Validate connection
                if not await validate_host(self.hass, host):
                    errors[CONF_HOST] = "cannot_connect"

            if not errors:
                # Create entry
                title = user_input.get(CONF_NAME) or f"Fox Energy {host}"
                return self.async_create_entry(
                    title=title,
                    data={
                        CONF_HOST: host,
                        CONF_TIMEOUT: user_input[CONF_TIMEOUT],
                        CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                    },
                )

        # First, try discovery
        if not self.discovered_devices:
            _LOGGER.info("Starting network scan for Fox Energy devices...")
            self.discovered_devices = await scan_network_for_devices(self.hass)
            _LOGGER.info(
                "Found %d Fox Energy devices: %s",
                len(self.discovered_devices),
                self.discovered_devices,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "discovered": ", ".join(self.discovered_devices)
                if self.discovered_devices
                else "none"
            },
        )

    async def async_step_discovery(
        self, discovery_info: dict[str, Any]
    ) -> FlowResult:
        """Handle discovery step.

        Args:
            discovery_info: Discovery information

        Returns:
            Flow result
        """
        host = discovery_info.get(CONF_HOST)
        
        if not host:
            return self.async_abort(reason="invalid_discovery_info")

        # Check if already configured
        await self.async_set_unique_id(host)
        self._abort_if_unique_id_configured()

        # Validate connection
        if not await validate_host(self.hass, host):
            return self.async_abort(reason="cannot_connect")

        return self.async_show_form(
            step_id="discovery_confirm",
            description_placeholders={CONF_HOST: host},
        )

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle discovery confirmation.

        Args:
            user_input: User input

        Returns:
            Flow result
        """
        if user_input is not None:
            host = self.discovery_data.get(CONF_HOST)
            return self.async_create_entry(
                title=f"Fox Energy {host}",
                data={
                    CONF_HOST: host,
                    CONF_TIMEOUT: DEFAULT_TIMEOUT,
                    CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
                },
            )

        return self.async_show_form(
            step_id="discovery_confirm",
        )


class FoxEnergyOptionsFlow(config_entries.OptionsFlow):
    """Options flow for Fox Energy integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize options flow.

        Args:
            config_entry: Config entry
        """
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Initialize options flow.

        Args:
            user_input: User input

        Returns:
            Flow result
        """
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),
                ): int,
                vol.Optional(
                    CONF_TIMEOUT,
                    default=self.config_entry.options.get(
                        CONF_TIMEOUT, DEFAULT_TIMEOUT
                    ),
                ): int,
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
