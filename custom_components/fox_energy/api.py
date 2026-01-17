"""API client for Fox Energy meter."""

import asyncio
import logging
from typing import Any, Literal

import aiohttp

from .const import (
    DEVICE_TYPE_1PHASE,
    DEVICE_TYPE_3PHASE,
    ENDPOINT_CURRENT_PARAMETERS,
    ENDPOINT_TOTAL_ENERGY,
)

_LOGGER = logging.getLogger(__name__)


class FoxEnergyConnectionError(Exception):
    """Connection error to Fox Energy device."""


class FoxEnergyAuthError(Exception):
    """Authentication error."""


class FoxEnergyInvalidResponse(Exception):
    """Invalid response from device."""


class FoxEnergyAPI:
    """REST API client for Fox Energy meter."""

    def __init__(self, host: str, timeout: int = 30):
        """Initialize the API client.

        Args:
            host: Device IP address (e.g., 192.168.3.101)
            timeout: Request timeout in seconds
        """
        self.host = host
        self.timeout = timeout
        self.base_url = f"http://{host}"

    async def get_current_parameters(self) -> dict[str, Any]:
        """Get current parameters (voltage, current, power, etc.).

        Returns:
            Dictionary with current parameters
            3-phase: lists with [L1, L2, L3] values
            1-phase: string values
        """
        return await self._get_endpoint(ENDPOINT_CURRENT_PARAMETERS)

    async def get_total_energy(self) -> dict[str, Any]:
        """Get total energy (import, export).

        Returns:
            Dictionary with energy values in Wh
            3-phase: lists with [L1, L2, L3] values
            1-phase: string values
        """
        return await self._get_endpoint(ENDPOINT_TOTAL_ENERGY)

    async def detect_device_type(self) -> Literal["3phase", "1phase"]:
        """Detect device type based on API response.

        Returns:
            "3phase" if device has 3 phases
            "1phase" if device is single-phase
        """
        try:
            data = await self.get_current_parameters()
            
            # Check if voltage is a list (3-phase) or string (1-phase)
            if isinstance(data.get("voltage"), list):
                return DEVICE_TYPE_3PHASE
            return DEVICE_TYPE_1PHASE
        except Exception as err:
            _LOGGER.error("Error detecting device type: %s", err)
            raise FoxEnergyInvalidResponse(f"Cannot detect device type: {err}") from err

    async def _get_endpoint(self, endpoint: str) -> dict[str, Any]:
        """Get data from endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            JSON response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get("status") != "ok":
                            raise FoxEnergyInvalidResponse(
                                f"Invalid response status: {data.get('status')}"
                            )
                        
                        return data
                    
                    raise FoxEnergyConnectionError(
                        f"HTTP {response.status}: {await response.text()}"
                    )
        except asyncio.TimeoutError as err:
            raise FoxEnergyConnectionError(f"Connection timeout to {self.host}") from err
        except aiohttp.ClientConnectorError as err:
            raise FoxEnergyConnectionError(f"Cannot connect to {self.host}") from err
        except aiohttp.ClientError as err:
            raise FoxEnergyConnectionError(f"Connection error: {err}") from err


class FoxEnergyDataProcessor:
    """Process raw API data into unified format."""

    @staticmethod
    def parse_energy_wh(value: Any) -> float:
        """Convert energy value from Wh to kWh.

        Args:
            value: Energy value (int or string with leading zeros)

        Returns:
            Energy in kWh rounded to 3 decimals
        """
        try:
            # Convert to int first (handles strings with leading zeros)
            wh = int(value) if isinstance(value, str) else float(value)
            kwh = wh / 1000
            return round(kwh, 3)
        except (ValueError, TypeError) as err:
            _LOGGER.error("Error parsing energy value %s: %s", value, err)
            return 0.0

    @staticmethod
    def parse_float(value: Any) -> float:
        """Convert value to float.

        Args:
            value: Value to convert (int, float, or string)

        Returns:
            Float value or 0.0 on error
        """
        try:
            return float(value) if value is not None else 0.0
        except (ValueError, TypeError) as err:
            _LOGGER.error("Error parsing float value %s: %s", value, err)
            return 0.0

    @classmethod
    def process_3phase_data(
        cls,
        current_params: dict[str, Any],
        total_energy: dict[str, Any],
    ) -> dict[str, Any]:
        """Process 3-phase device data.

        Args:
            current_params: Current parameters response
            total_energy: Total energy response

        Returns:
            Unified dictionary with all sensor data
        """
        result = {
            # Energy (kWh)
            "energia_pobrana_l1": cls.parse_energy_wh(total_energy["active_energy_import"][0]),
            "energia_pobrana_l2": cls.parse_energy_wh(total_energy["active_energy_import"][1]),
            "energia_pobrana_l3": cls.parse_energy_wh(total_energy["active_energy_import"][2]),
            # Power (W)
            "moc_czynna_l1": cls.parse_float(current_params["power_active"][0]),
            "moc_czynna_l2": cls.parse_float(current_params["power_active"][1]),
            "moc_czynna_l3": cls.parse_float(current_params["power_active"][2]),
            # Current (A)
            "natezenie_l1": cls.parse_float(current_params["current"][0]),
            "natezenie_l2": cls.parse_float(current_params["current"][1]),
            "natezenie_l3": cls.parse_float(current_params["current"][2]),
            # Voltage (V)
            "napiecie_l1": cls.parse_float(current_params["voltage"][0]),
            "napiecie_l2": cls.parse_float(current_params["voltage"][1]),
            "napiecie_l3": cls.parse_float(current_params["voltage"][2]),
            # Reactive Power (VAr)
            "moc_reaktywna_l1": cls.parse_float(current_params["power_reactive"][0]),
            "moc_reaktywna_l2": cls.parse_float(current_params["power_reactive"][1]),
            "moc_reaktywna_l3": cls.parse_float(current_params["power_reactive"][2]),
            # Power Factor (cos φ)
            "cos_phi_l1": cls.parse_float(current_params["power_factor"][0]),
            "cos_phi_l2": cls.parse_float(current_params["power_factor"][1]),
            "cos_phi_l3": cls.parse_float(current_params["power_factor"][2]),
            # Frequency (Hz)
            "czestotliwosc_l1": cls.parse_float(current_params["frequency"][0]),
            "czestotliwosc_l2": cls.parse_float(current_params["frequency"][1]),
            "czestotliwosc_l3": cls.parse_float(current_params["frequency"][2]),
        }

        # Calculate sums
        result["energia_pobrana_suma"] = round(
            result["energia_pobrana_l1"]
            + result["energia_pobrana_l2"]
            + result["energia_pobrana_l3"],
            3,
        )
        result["moc_czynna_suma"] = round(
            result["moc_czynna_l1"]
            + result["moc_czynna_l2"]
            + result["moc_czynna_l3"],
            1,
        )
        result["natezenie_suma"] = round(
            result["natezenie_l1"]
            + result["natezenie_l2"]
            + result["natezenie_l3"],
            2,
        )

        return result

    @classmethod
    def process_1phase_data(
        cls,
        current_params: dict[str, Any],
        total_energy: dict[str, Any],
    ) -> dict[str, Any]:
        """Process 1-phase device data.

        Args:
            current_params: Current parameters response (string values)
            total_energy: Total energy response (string values)

        Returns:
            Unified dictionary with all sensor data
        """
        result = {
            # Energy (kWh)
            "energia_pobrana": cls.parse_energy_wh(total_energy["active_energy"]),
            # Power (W)
            "moc_czynna": cls.parse_float(current_params["power_active"]),
            # Current (A)
            "natezenie": cls.parse_float(current_params["current"]),
            # Voltage (V)
            "napiecie": cls.parse_float(current_params["voltage"]),
            # Reactive Power (VAr)
            "moc_reaktywna": cls.parse_float(current_params["power_reactive"]),
            # Power Factor (cos φ)
            "cos_phi": cls.parse_float(current_params["power_factor"]),
            # Frequency (Hz)
            "czestotliwosc": cls.parse_float(current_params["frequency"]),
        }

        return result
