"""Tests for Fox Energy API client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.fox_energy.api import (
    FoxEnergyAPI,
    FoxEnergyConnectionError,
    FoxEnergyDataProcessor,
    FoxEnergyInvalidResponse,
)
from custom_components.fox_energy.const import DEVICE_TYPE_1PHASE, DEVICE_TYPE_3PHASE


class TestFoxEnergyAPI:
    """Tests for FoxEnergyAPI class."""

    def test_init(self):
        """Test API initialization."""
        api = FoxEnergyAPI("192.168.1.100", timeout=30)
        assert api.host == "192.168.1.100"
        assert api.timeout == 30
        assert api.base_url == "http://192.168.1.100"

    def test_init_default_timeout(self):
        """Test API initialization with default timeout."""
        api = FoxEnergyAPI("192.168.1.100")
        assert api.timeout == 30

    @pytest.mark.asyncio
    async def test_get_current_parameters_success(self, mock_3phase_current):
        """Test successful current parameters fetch."""
        api = FoxEnergyAPI("192.168.1.100")

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_3phase_current)

        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = MagicMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)
            mock_session.get = MagicMock(return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response),
                __aexit__=AsyncMock(return_value=None)
            ))
            mock_session_class.return_value = mock_session

            result = await api.get_current_parameters()

        assert result["status"] == "ok"
        assert result["voltage"] == [239.7, 243.7, 234.6]

    @pytest.mark.asyncio
    async def test_get_endpoint_invalid_status(self):
        """Test API response with invalid status."""
        api = FoxEnergyAPI("192.168.1.100")

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"status": "error"})

        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = MagicMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)
            mock_session.get = MagicMock(return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response),
                __aexit__=AsyncMock(return_value=None)
            ))
            mock_session_class.return_value = mock_session

            with pytest.raises(FoxEnergyInvalidResponse):
                await api.get_current_parameters()

    @pytest.mark.asyncio
    async def test_get_endpoint_http_error(self):
        """Test API HTTP error handling."""
        api = FoxEnergyAPI("192.168.1.100")

        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text = AsyncMock(return_value="Internal Server Error")

        with patch("aiohttp.ClientSession") as mock_session_class:
            mock_session = MagicMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)
            mock_session.get = MagicMock(return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response),
                __aexit__=AsyncMock(return_value=None)
            ))
            mock_session_class.return_value = mock_session

            with pytest.raises(FoxEnergyConnectionError) as exc_info:
                await api.get_current_parameters()

            assert "HTTP 500" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_detect_device_type_3phase(self, mock_3phase_current):
        """Test 3-phase device detection."""
        api = FoxEnergyAPI("192.168.1.100")

        with patch.object(api, "get_current_parameters", return_value=mock_3phase_current):
            device_type = await api.detect_device_type()

        assert device_type == DEVICE_TYPE_3PHASE

    @pytest.mark.asyncio
    async def test_detect_device_type_1phase(self, mock_1phase_current):
        """Test 1-phase device detection."""
        api = FoxEnergyAPI("192.168.1.100")

        with patch.object(api, "get_current_parameters", return_value=mock_1phase_current):
            device_type = await api.detect_device_type()

        assert device_type == DEVICE_TYPE_1PHASE


class TestFoxEnergyDataProcessor:
    """Tests for FoxEnergyDataProcessor class."""

    def test_parse_energy_wh_int(self):
        """Test energy parsing from integer."""
        result = FoxEnergyDataProcessor.parse_energy_wh(1000)
        assert result == 1.0

    def test_parse_energy_wh_string(self):
        """Test energy parsing from string with leading zeros."""
        result = FoxEnergyDataProcessor.parse_energy_wh("01871193477")
        assert result == 1871193.477

    def test_parse_energy_wh_invalid(self):
        """Test energy parsing with invalid value."""
        result = FoxEnergyDataProcessor.parse_energy_wh("invalid")
        assert result == 0.0

    def test_parse_energy_wh_none(self):
        """Test energy parsing with None."""
        result = FoxEnergyDataProcessor.parse_energy_wh(None)
        assert result == 0.0

    def test_parse_float_string(self):
        """Test float parsing from string."""
        result = FoxEnergyDataProcessor.parse_float("234.8")
        assert result == 234.8

    def test_parse_float_int(self):
        """Test float parsing from int."""
        result = FoxEnergyDataProcessor.parse_float(100)
        assert result == 100.0

    def test_parse_float_none(self):
        """Test float parsing with None."""
        result = FoxEnergyDataProcessor.parse_float(None)
        assert result == 0.0

    def test_parse_float_invalid(self):
        """Test float parsing with invalid value."""
        result = FoxEnergyDataProcessor.parse_float("invalid")
        assert result == 0.0

    def test_process_3phase_data(self, mock_3phase_current, mock_3phase_energy):
        """Test 3-phase data processing."""
        result = FoxEnergyDataProcessor.process_3phase_data(
            mock_3phase_current, mock_3phase_energy
        )

        # Check energy values (converted from Wh to kWh)
        assert result["energia_pobrana_l1"] == 4951.294
        assert result["energia_pobrana_l2"] == 1326.375
        assert result["energia_pobrana_l3"] == 6228.263

        # Check sum
        assert result["energia_pobrana_suma"] == 12505.932

        # Check power values
        assert result["moc_czynna_l1"] == 353.6
        assert result["moc_czynna_l2"] == 40.3
        assert result["moc_czynna_l3"] == 69.7
        assert result["moc_czynna_suma"] == 463.6

        # Check voltage
        assert result["napiecie_l1"] == 239.7
        assert result["napiecie_l2"] == 243.7
        assert result["napiecie_l3"] == 234.6

        # Check current
        assert result["natezenie_l1"] == 1.97
        assert result["natezenie_l2"] == 0.49
        assert result["natezenie_l3"] == 1.08
        assert result["natezenie_suma"] == 3.54

        # Check frequency
        assert result["czestotliwosc_l1"] == 50.010
        assert result["czestotliwosc_l2"] == 50.010
        assert result["czestotliwosc_l3"] == 50.010

        # Check power factor
        assert result["cos_phi_l1"] == -0.75
        assert result["cos_phi_l2"] == -0.34
        assert result["cos_phi_l3"] == -0.27

    def test_process_1phase_data(self, mock_1phase_current, mock_1phase_energy):
        """Test 1-phase data processing."""
        result = FoxEnergyDataProcessor.process_1phase_data(
            mock_1phase_current, mock_1phase_energy
        )

        # Check energy (converted from Wh to kWh)
        assert result["energia_pobrana"] == 1871193.477

        # Check power
        assert result["moc_czynna"] == 3.0

        # Check voltage
        assert result["napiecie"] == 234.8

        # Check current
        assert result["natezenie"] == 0.0

        # Check frequency
        assert result["czestotliwosc"] == 50.0

        # Check power factor
        assert result["cos_phi"] == -0.48

        # Check reactive power
        assert result["moc_reaktywna"] == 0.0
