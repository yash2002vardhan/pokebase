import pytest
import aiohttp
from aioresponses import aioresponses
from unittest.mock import patch
from app.service.pokemon import PokemonService, get_pokemon_service


@pytest.mark.unit
class TestPokemonService:
    """Unit tests for PokemonService"""

    @pytest.fixture
    def pokemon_service(self, test_settings):
        """Create a PokemonService instance for testing"""
        with patch('app.service.pokemon.settings', test_settings):
            return PokemonService()

    @pytest.mark.asyncio
    async def test_get_pokemon_data_success(self, pokemon_service, sample_pokemon_data):
        """Test successful Pokemon data retrieval"""
        pokemon_name = "pikachu"
        url = f"{pokemon_service.base_url}/pokemon/{pokemon_name}"
        
        with aioresponses() as m:
            m.get(url, payload=sample_pokemon_data)
            
            result = await pokemon_service.get_pokemon_data(pokemon_name)
            assert result == sample_pokemon_data

    @pytest.mark.asyncio
    async def test_get_pokemon_data_not_found(self, pokemon_service):
        """Test handling of Pokemon not found (404)"""
        pokemon_name = "nonexistent"
        url = f"{pokemon_service.base_url}/pokemon/{pokemon_name}"
        
        with aioresponses() as m:
            m.get(url, status=404)
            
            with pytest.raises(Exception, match="Pokemon nonexistent not found"):
                await pokemon_service.get_pokemon_data(pokemon_name)

    @pytest.mark.asyncio
    async def test_get_pokemon_data_http_error(self, pokemon_service):
        """Test handling of HTTP errors"""
        pokemon_name = "pikachu"
        url = f"{pokemon_service.base_url}/pokemon/{pokemon_name}"
        error_response = {"error": "Server error"}
        
        with aioresponses() as m:
            m.get(url, status=500, payload=error_response)
            
            result = await pokemon_service.get_pokemon_data(pokemon_name)
            assert result == error_response

    @pytest.mark.asyncio
    async def test_get_pokemon_data_network_error(self, pokemon_service):
        """Test handling of network errors"""
        pokemon_name = "pikachu"
        url = f"{pokemon_service.base_url}/pokemon/{pokemon_name}"
        
        with aioresponses() as m:
            m.get(url, exception=aiohttp.ClientError("Network error"))
            
            with pytest.raises(aiohttp.ClientError, match="Network error"):
                await pokemon_service.get_pokemon_data(pokemon_name)

    @pytest.mark.asyncio
    async def test_get_pokemon_data_json_decode_error(self, pokemon_service):
        """Test handling of JSON decode errors"""
        pokemon_name = "pikachu"
        url = f"{pokemon_service.base_url}/pokemon/{pokemon_name}"
        
        with aioresponses() as m:
            # Return invalid JSON
            m.get(url, body="invalid json", content_type="text/plain")
            
            with pytest.raises(Exception):  # Should raise JSON decode error
                await pokemon_service.get_pokemon_data(pokemon_name)

    def test_init_with_base_url(self, test_settings):
        """Test PokemonService initialization with correct base URL"""
        with patch('app.service.pokemon.settings', test_settings):
            service = PokemonService()
            assert service.base_url == test_settings.POKEMON_API_URL

    @pytest.mark.asyncio
    async def test_get_pokemon_service_dependency(self):
        """Test the dependency injection function"""
        service = await get_pokemon_service()
        assert isinstance(service, PokemonService)

    @pytest.mark.asyncio
    async def test_pokemon_data_with_special_characters(self, pokemon_service, sample_pokemon_data):
        """Test Pokemon data retrieval with special characters in name"""
        pokemon_name = "nidoran♀"
        url = f"{pokemon_service.base_url}/pokemon/{pokemon_name}"
        
        with aioresponses() as m:
            m.get(url, payload=sample_pokemon_data)
            
            result = await pokemon_service.get_pokemon_data(pokemon_name)
            assert result == sample_pokemon_data

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, pokemon_service, sample_pokemon_data):
        """Test handling of concurrent requests"""
        pokemon_names = ["pikachu", "charizard", "blastoise"]
        
        with aioresponses() as m:
            # Mock all Pokemon URLs
            for name in pokemon_names:
                url = f"{pokemon_service.base_url}/pokemon/{name}"
                m.get(url, payload=sample_pokemon_data)
            
            # Execute concurrent requests
            import asyncio
            tasks = [
                pokemon_service.get_pokemon_data(name) 
                for name in pokemon_names
            ]
            results = await asyncio.gather(*tasks)
            
            # Verify all requests succeeded
            assert len(results) == 3
            assert all(result == sample_pokemon_data for result in results) 
