"""Tests for Fox Energy constants."""

from custom_components.fox_energy.const import (
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
    DEVICE_TYPE_1PHASE,
    DEVICE_TYPE_3PHASE,
    DOMAIN,
    ENDPOINT_CURRENT_PARAMETERS,
    ENDPOINT_TOTAL_ENERGY,
    ERROR_CANNOT_CONNECT,
    ERROR_INVALID_RESPONSE,
    MANUFACTURER,
    SENSORS_1PHASE,
    SENSORS_3PHASE,
)


class TestConstants:
    """Tests for integration constants."""

    def test_domain(self):
        """Test domain constant."""
        assert DOMAIN == "fox_energy"

    def test_manufacturer(self):
        """Test manufacturer constant."""
        assert MANUFACTURER == "F&F"

    def test_default_values(self):
        """Test default configuration values."""
        assert DEFAULT_TIMEOUT == 30
        assert DEFAULT_SCAN_INTERVAL == 5

    def test_endpoints(self):
        """Test API endpoints."""
        assert ENDPOINT_CURRENT_PARAMETERS == "/0000/get_current_parameters"
        assert ENDPOINT_TOTAL_ENERGY == "/0000/get_total_energy"

    def test_device_types(self):
        """Test device type constants."""
        assert DEVICE_TYPE_3PHASE == "3phase"
        assert DEVICE_TYPE_1PHASE == "1phase"

    def test_error_messages(self):
        """Test error message constants."""
        assert ERROR_CANNOT_CONNECT == "cannot_connect"
        assert ERROR_INVALID_RESPONSE == "invalid_response"

    def test_conf_scan_interval(self):
        """Test config flow constants."""
        assert CONF_SCAN_INTERVAL == "scan_interval"


class TestSensorConfigurations:
    """Tests for sensor configuration dictionaries."""

    def test_3phase_sensors_count(self):
        """Test 3-phase sensor count."""
        assert len(SENSORS_3PHASE) == 24

    def test_1phase_sensors_count(self):
        """Test 1-phase sensor count."""
        assert len(SENSORS_1PHASE) == 7

    def test_3phase_sensor_keys(self):
        """Test 3-phase sensor keys exist."""
        expected_keys = [
            "energia_pobrana_l1",
            "energia_pobrana_l2",
            "energia_pobrana_l3",
            "energia_pobrana_suma",
            "moc_czynna_l1",
            "moc_czynna_l2",
            "moc_czynna_l3",
            "moc_czynna_suma",
            "natezenie_l1",
            "natezenie_l2",
            "natezenie_l3",
            "natezenie_suma",
            "napiecie_l1",
            "napiecie_l2",
            "napiecie_l3",
        ]
        for key in expected_keys:
            assert key in SENSORS_3PHASE, f"Missing key: {key}"

    def test_1phase_sensor_keys(self):
        """Test 1-phase sensor keys exist."""
        expected_keys = [
            "energia_pobrana",
            "moc_czynna",
            "natezenie",
            "napiecie",
            "moc_reaktywna",
            "cos_phi",
            "czestotliwosc",
        ]
        for key in expected_keys:
            assert key in SENSORS_1PHASE, f"Missing key: {key}"

    def test_sensor_config_structure(self):
        """Test sensor configuration structure."""
        required_fields = ["name", "unit", "device_class", "state_class", "icon"]

        for key, config in SENSORS_3PHASE.items():
            for field in required_fields:
                assert field in config, f"Missing field '{field}' in sensor '{key}'"

        for key, config in SENSORS_1PHASE.items():
            for field in required_fields:
                assert field in config, f"Missing field '{field}' in sensor '{key}'"

    def test_energy_sensors_device_class(self):
        """Test energy sensors have correct device class."""
        energy_sensors_3phase = [
            "energia_pobrana_l1",
            "energia_pobrana_l2",
            "energia_pobrana_l3",
            "energia_pobrana_suma",
        ]
        for key in energy_sensors_3phase:
            assert SENSORS_3PHASE[key]["device_class"] == "energy"
            assert SENSORS_3PHASE[key]["state_class"] == "total_increasing"
            assert SENSORS_3PHASE[key]["unit"] == "kWh"

        assert SENSORS_1PHASE["energia_pobrana"]["device_class"] == "energy"
        assert SENSORS_1PHASE["energia_pobrana"]["state_class"] == "total_increasing"

    def test_power_sensors_device_class(self):
        """Test power sensors have correct device class."""
        power_sensors_3phase = [
            "moc_czynna_l1",
            "moc_czynna_l2",
            "moc_czynna_l3",
            "moc_czynna_suma",
        ]
        for key in power_sensors_3phase:
            assert SENSORS_3PHASE[key]["device_class"] == "power"
            assert SENSORS_3PHASE[key]["state_class"] == "measurement"
            assert SENSORS_3PHASE[key]["unit"] == "W"

    def test_voltage_sensors_device_class(self):
        """Test voltage sensors have correct device class."""
        voltage_sensors = ["napiecie_l1", "napiecie_l2", "napiecie_l3"]
        for key in voltage_sensors:
            assert SENSORS_3PHASE[key]["device_class"] == "voltage"
            assert SENSORS_3PHASE[key]["unit"] == "V"

    def test_current_sensors_device_class(self):
        """Test current sensors have correct device class."""
        current_sensors = [
            "natezenie_l1",
            "natezenie_l2",
            "natezenie_l3",
            "natezenie_suma",
        ]
        for key in current_sensors:
            assert SENSORS_3PHASE[key]["device_class"] == "current"
            assert SENSORS_3PHASE[key]["unit"] == "A"

    def test_frequency_sensors_device_class(self):
        """Test frequency sensors have correct device class."""
        freq_sensors = ["czestotliwosc_l1", "czestotliwosc_l2", "czestotliwosc_l3"]
        for key in freq_sensors:
            assert SENSORS_3PHASE[key]["device_class"] == "frequency"
            assert SENSORS_3PHASE[key]["unit"] == "Hz"
