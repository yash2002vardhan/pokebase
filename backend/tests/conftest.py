import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
import asyncio
from app.main import app
from app.config.env import Settings

# Test data fixtures
@pytest.fixture
def sample_pokemon_data():
    """Sample Pokemon data for testing"""
    return {
        "id": 25,
        "name": "pikachu",
        "base_experience": 112,
        "height": 4,
        "weight": 60,
        "species": {"name": "pikachu"},
        "abilities": [
            {
                "ability": {"name": "static"},
                "is_hidden": False
            },
            {
                "ability": {"name": "lightning-rod"},
                "is_hidden": True
            }
        ],
        "moves": [
            {"move": {"name": "thunder-shock"}},
            {"move": {"name": "tail-whip"}},
            {"move": {"name": "quick-attack"}}
        ],
        "types": [
            {"type": {"name": "electric"}}
        ],
        "stats": [
            {"stat": {"name": "hp"}, "base_stat": 35},
            {"stat": {"name": "attack"}, "base_stat": 55},
            {"stat": {"name": "defense"}, "base_stat": 40},
            {"stat": {"name": "special-attack"}, "base_stat": 50},
            {"stat": {"name": "special-defense"}, "base_stat": 50},
            {"stat": {"name": "speed"}, "base_stat": 90}
        ]
    }

@pytest.fixture
def test_settings():
    """Test settings for configuration"""
    return Settings(
        POKEMON_API_URL="https://pokeapi.co/api/v2",
        GEMINI_API_KEY="test-api-key"
    )

# HTTP Client fixtures
@pytest.fixture
def client():
    """Synchronous test client"""
    return TestClient(app)

@pytest.fixture
async def async_client():
    """Asynchronous test client"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# Mock fixtures for Pokemon service
@pytest.fixture
def mock_aiohttp_session():
    """Mock aiohttp session"""
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock()
    mock_session.get.return_value.__aenter__.return_value = mock_response
    return mock_session, mock_response

# Mock fixtures for API endpoints
@pytest.fixture
def mock_llm():
    """Mock LLM service for API endpoints"""
    mock = MagicMock()
    mock.generate_content.return_value = "Mock LLM response"
    return mock

@pytest.fixture
def mock_parse_pokemon_data():
    """Mock parse_pokemon_data function for API endpoints"""
    with patch('app.api.endpoints.parse_pokemon_data') as mock:
        yield mock

@pytest.fixture
def mock_generate_descriptions():
    """Mock generate_descriptions function for API endpoints"""
    with patch('app.api.endpoints.generate_descriptions') as mock:
        mock.return_value = "Generated Pokemon description"
        yield mock 
