"""Fixtures for Fox Energy integration tests."""

import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

# Mock homeassistant modules before any other imports
sys.modules["homeassistant"] = MagicMock()
sys.modules["homeassistant.config_entries"] = MagicMock()
sys.modules["homeassistant.const"] = MagicMock()
sys.modules["homeassistant.core"] = MagicMock()
sys.modules["homeassistant.helpers"] = MagicMock()
sys.modules["homeassistant.helpers.aiohttp_client"] = MagicMock()
sys.modules["homeassistant.helpers.entity"] = MagicMock()
sys.modules["homeassistant.helpers.entity_platform"] = MagicMock()
sys.modules["homeassistant.helpers.update_coordinator"] = MagicMock()
sys.modules["homeassistant.helpers.typing"] = MagicMock()
sys.modules["homeassistant.data_entry_flow"] = MagicMock()
sys.modules["homeassistant.util"] = MagicMock()
sys.modules["homeassistant.util.dt"] = MagicMock()
sys.modules["homeassistant.components"] = MagicMock()
sys.modules["homeassistant.components.sensor"] = MagicMock()
sys.modules["voluptuous"] = MagicMock()

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def mock_3phase_current():
    """Load 3-phase current parameters fixture."""
    with open(FIXTURES_DIR / "3phase_current.json") as f:
        return json.load(f)


@pytest.fixture
def mock_3phase_energy():
    """Load 3-phase energy fixture."""
    with open(FIXTURES_DIR / "3phase_energy.json") as f:
        return json.load(f)


@pytest.fixture
def mock_1phase_current():
    """Load 1-phase current parameters fixture."""
    with open(FIXTURES_DIR / "1phase_current.json") as f:
        return json.load(f)


@pytest.fixture
def mock_1phase_energy():
    """Load 1-phase energy fixture."""
    with open(FIXTURES_DIR / "1phase_energy.json") as f:
        return json.load(f)


@pytest.fixture
def mock_aiohttp_session():
    """Create mock aiohttp session."""
    session = MagicMock()
    session.get = AsyncMock()
    return session


@pytest.fixture
def mock_response_ok():
    """Create mock successful HTTP response."""
    response = AsyncMock()
    response.status = 200
    return response


@pytest.fixture
def mock_response_error():
    """Create mock error HTTP response."""
    response = AsyncMock()
    response.status = 500
    response.text = AsyncMock(return_value="Internal Server Error")
    return response
