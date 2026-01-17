"""Base entity for Fox Energy integration."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import FoxEnergyCoordinator


class FoxEnergyEntity(CoordinatorEntity[FoxEnergyCoordinator]):
    """Base entity for Fox Energy devices."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: FoxEnergyCoordinator, sensor_key: str):
        """Initialize entity.

        Args:
            coordinator: Data update coordinator
            sensor_key: Unique sensor identifier
        """
        super().__init__(coordinator)
        self.sensor_key = sensor_key

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        host = self.coordinator.host
        return DeviceInfo(
            identifiers={(DOMAIN, host)},
            name=f"Fox Energy ({host})",
            manufacturer=MANUFACTURER,
            model=self.coordinator.device_type,
        )


class FoxEnergySensor(FoxEnergyEntity, SensorEntity):
    """Fox Energy sensor entity."""

    def __init__(
        self,
        coordinator: FoxEnergyCoordinator,
        sensor_key: str,
        sensor_config: dict,
    ):
        """Initialize sensor.

        Args:
            coordinator: Data update coordinator
            sensor_key: Unique sensor identifier
            sensor_config: Sensor configuration dict with name, unit, etc.
        """
        super().__init__(coordinator, sensor_key)

        self._attr_name = sensor_config.get("name")
        self._attr_native_unit_of_measurement = sensor_config.get("unit")
        self._attr_device_class = sensor_config.get("device_class")
        self._attr_state_class = sensor_config.get("state_class")
        self._attr_icon = sensor_config.get("icon")
        self._attr_unique_id = f"{coordinator.host}_{sensor_key}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.sensor_key)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success and self.coordinator.data is not None
        )
