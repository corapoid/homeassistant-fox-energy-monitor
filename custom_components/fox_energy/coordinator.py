"""Data update coordinator for Fox Energy integration."""

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util.dt import utcnow

from .api import (
    FoxEnergyAPI,
    FoxEnergyConnectionError,
    FoxEnergyDataProcessor,
    FoxEnergyInvalidResponse,
)
from .const import (
    DEFAULT_SCAN_INTERVAL,
    DEVICE_TYPE_1PHASE,
    DEVICE_TYPE_3PHASE,
)

_LOGGER = logging.getLogger(__name__)


class FoxEnergyCoordinator(DataUpdateCoordinator):
    """Data update coordinator for Fox Energy meter."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        timeout: int = 30,
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
    ):
        """Initialize coordinator.

        Args:
            hass: Home Assistant instance
            host: Device IP address
            timeout: Request timeout in seconds
            scan_interval: Update interval in seconds
        """
        from datetime import timedelta

        super().__init__(
            hass,
            _LOGGER,
            name=f"Fox Energy {host}",
            update_interval=timedelta(seconds=scan_interval),
        )

        self.host = host
        self.api = FoxEnergyAPI(host, timeout)
        self.device_type: str | None = None
        self.model: str | None = None

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from device.

        Returns:
            Unified data dictionary

        Raises:
            UpdateFailed: If data fetch fails
        """
        try:
            # Detect device type on first run
            if self.device_type is None:
                self.device_type = await self.api.detect_device_type()
                _LOGGER.info(
                    "Fox Energy device at %s detected as %s",
                    self.host,
                    self.device_type,
                )

            # Fetch both endpoints
            current_params = await self.api.get_current_parameters()
            total_energy = await self.api.get_total_energy()

            # Process data based on device type
            if self.device_type == DEVICE_TYPE_3PHASE:
                data = FoxEnergyDataProcessor.process_3phase_data(
                    current_params, total_energy
                )
            else:
                data = FoxEnergyDataProcessor.process_1phase_data(
                    current_params, total_energy
                )

            # Add metadata
            data["last_update"] = utcnow()
            data["device_type"] = self.device_type

            return data

        except FoxEnergyConnectionError as err:
            raise UpdateFailed(f"Connection error: {err}") from err
        except FoxEnergyInvalidResponse as err:
            raise UpdateFailed(f"Invalid response: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error updating data: %s", err)
            raise UpdateFailed(f"Unexpected error: {err}") from err
