"""Sensors for Fox Energy integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DEVICE_TYPE_3PHASE, DOMAIN, SENSORS_1PHASE, SENSORS_3PHASE
from .coordinator import FoxEnergyCoordinator
from .entity import FoxEnergySensor

_LOGGER = logging.getLogger(__name__)


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
    coordinator: FoxEnergyCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    if coordinator.device_type == DEVICE_TYPE_3PHASE:
        sensors_config = SENSORS_3PHASE
    else:
        sensors_config = SENSORS_1PHASE

    entities = [
        FoxEnergySensor(coordinator, sensor_key, sensor_config)
        for sensor_key, sensor_config in sensors_config.items()
    ]

    async_add_entities(entities)
