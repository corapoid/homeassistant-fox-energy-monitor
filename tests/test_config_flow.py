"""Tests for Fox Energy config flow.

Note: Full config_flow tests require Python 3.10+ due to union type syntax.
These tests focus on constants and basic validation that can run on Python 3.9+.
"""

from custom_components.fox_energy.const import (
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
    DOMAIN,
)


class TestConfigFlowConstants:
    """Tests for config flow constants."""

    def test_default_values(self):
        """Test default configuration values."""
        assert DEFAULT_TIMEOUT == 30
        assert DEFAULT_SCAN_INTERVAL == 5
        assert DOMAIN == "fox_energy"

    def test_conf_scan_interval(self):
        """Test scan interval constant."""
        assert CONF_SCAN_INTERVAL == "scan_interval"

    def test_default_scan_interval_value(self):
        """Test that default scan interval is 5 seconds as required."""
        assert DEFAULT_SCAN_INTERVAL == 5

    def test_domain_format(self):
        """Test domain is valid snake_case format."""
        assert "_" in DOMAIN or DOMAIN.islower()
        assert " " not in DOMAIN
        assert DOMAIN.replace("_", "").isalnum()
