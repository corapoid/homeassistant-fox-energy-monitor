"""Config flow for Fox Energy integration."""

import ipaddress
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_TIMEOUT
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from .api import FoxEnergyAPI, FoxEnergyConnectionError, FoxEnergyInvalidResponse
from .const import CONF_HOST, CONF_SCAN_INTERVAL, DEFAULT_TIMEOUT, DEFAULT_SCAN_INTERVAL, DOMAIN

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


class FoxEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Fox Energy integration."""

    VERSION = 1

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
            host = user_input.get(CONF_HOST, "").strip()

            # Validate IP address format
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

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
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
