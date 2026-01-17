"""Sensors for Fox Energy integration."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DEVICE_TYPE_1PHASE, DEVICE_TYPE_3PHASE, SENSORS_1PHASE, SENSORS_3PHASE
from .coordinator import FoxEnergyCoordinator
from .entity import FoxEnergySensor

_LOGGER = logging.getLogger(__name__)

PLATFORM = Platform.SENSOR


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Fox Energy sensors from config entry.

    Args:
        hass: Home Assistant instance
        config_entry: Config entry
        async_add_entities: Callback to add entities
    """
    coordinator: FoxEnergyCoordinator = hass.data[DEVICE_TYPE_3PHASE][config_entry.entry_id]

    # Wait for first data fetch to determine device type
    await coordinator.async_config_entry_first_refresh()

    if coordinator.device_type == DEVICE_TYPE_3PHASE:
        sensors_config = SENSORS_3PHASE
    else:
        sensors_config = SENSORS_1PHASE

    entities = [
        FoxEnergySensor(coordinator, sensor_key, sensor_config)
        for sensor_key, sensor_config in sensors_config.items()
    ]

    async_add_entities(entities)


class FoxEnergySensorEntity(FoxEnergySensor):
    """Extended Fox Energy sensor with additional properties."""

    _attr_has_entity_name = True

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
        )

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None

        value = self.coordinator.data.get(self.sensor_key)
        return value

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from coordinator."""
        self.async_write_ha_state()
