import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException
from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.mark.integration
class TestHealthEndpoint:
    """Integration tests for health check endpoint"""

    def test_health_check_success(self, client):
        """Test health check endpoint returns healthy status"""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    @pytest.mark.asyncio
    async def test_health_check_async(self, async_client):
        """Test health check endpoint with async client"""
        response = await async_client.get("/api/v1/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


@pytest.mark.integration
class TestPokemonEndpoints:
    """Integration tests for Pokemon endpoints"""

    def test_get_pokemon_success(self, client, mock_parse_pokemon_data, mock_generate_descriptions):
        """Test successful Pokemon retrieval"""
        pokemon_name = "pikachu"
        mock_parse_pokemon_data.return_value = {"name": pokemon_name}
        mock_generate_descriptions.return_value = "Pikachu description"
        
        response = client.get(f"/api/v1/pokemon/{pokemon_name}")
        
        assert response.status_code == 200
        assert response.json() == "Pikachu description"
        mock_parse_pokemon_data.assert_called_once_with(pokemon_name.lower())

    def test_get_pokemon_not_found(self, client, mock_parse_pokemon_data):
        """Test Pokemon not found error handling"""
        pokemon_name = "nonexistent"
        mock_parse_pokemon_data.side_effect = Exception("Pokemon not found")
        
        response = client.get(f"/api/v1/pokemon/{pokemon_name}")
        
        assert response.status_code == 404
        assert "Pokemon not found" in response.json()["detail"]

    def test_get_pokemon_case_insensitive(self, client, mock_parse_pokemon_data, mock_generate_descriptions):
        """Test Pokemon name is case insensitive"""
        pokemon_name = "PIKACHU"
        mock_parse_pokemon_data.return_value = {"name": "pikachu"}
        mock_generate_descriptions.return_value = "Pikachu description"
        
        response = client.get(f"/api/v1/pokemon/{pokemon_name}")
        
        assert response.status_code == 200
        mock_parse_pokemon_data.assert_called_once_with("pikachu")

    @pytest.mark.asyncio
    async def test_get_pokemon_async(self, async_client, mock_parse_pokemon_data, mock_generate_descriptions):
        """Test Pokemon retrieval with async client"""
        pokemon_name = "pikachu"
        mock_parse_pokemon_data.return_value = {"name": pokemon_name}
        mock_generate_descriptions.return_value = "Pikachu description"
        
        response = await async_client.get(f"/api/v1/pokemon/{pokemon_name}")
        
        assert response.status_code == 200
        assert response.json() == "Pikachu description"

    def test_compare_pokemon_success(self, client, mock_parse_pokemon_data, mock_generate_descriptions):
        """Test successful Pokemon comparison"""
        pokemon1 = "pikachu"
        pokemon2 = "charizard"
        
        # Setup mock return values
        mock_parse_pokemon_data.side_effect = [
            {"name": pokemon1},
            {"name": pokemon2}
        ]
        mock_generate_descriptions.side_effect = [
            "Pikachu description",
            "Charizard description"
        ]
        
        response = client.get(f"/api/v1/pokemon/compare/{pokemon1}/{pokemon2}")
        
        assert response.status_code == 200
        expected_response = "Pikachu description\n\nCharizard description"
        assert response.json() == expected_response
        
        # Verify both Pokemon were parsed
        assert mock_parse_pokemon_data.call_count == 2
        assert mock_generate_descriptions.call_count == 2

    def test_compare_pokemon_first_not_found(self, client, mock_parse_pokemon_data):
        """Test comparison when first Pokemon is not found"""
        pokemon1 = "nonexistent"
        pokemon2 = "pikachu"
        
        mock_parse_pokemon_data.side_effect = Exception("Pokemon not found")
        
        response = client.get(f"/api/v1/pokemon/compare/{pokemon1}/{pokemon2}")
        
        assert response.status_code == 404
        assert "Pokemon not found" in response.json()["detail"]

    def test_compare_pokemon_second_not_found(self, client, mock_parse_pokemon_data, mock_generate_descriptions):
        """Test comparison when second Pokemon is not found"""
        pokemon1 = "pikachu"
        pokemon2 = "nonexistent"
        
        # First call succeeds, second fails
        mock_parse_pokemon_data.side_effect = [
            {"name": pokemon1},
            Exception("Pokemon not found")
        ]
        
        response = client.get(f"/api/v1/pokemon/compare/{pokemon1}/{pokemon2}")
        
        assert response.status_code == 404
        assert "Pokemon not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_compare_pokemon_async(self, async_client, mock_parse_pokemon_data, mock_generate_descriptions):
        """Test Pokemon comparison with async client"""
        pokemon1 = "pikachu"
        pokemon2 = "charizard"
        
        mock_parse_pokemon_data.side_effect = [
            {"name": pokemon1},
            {"name": pokemon2}
        ]
        mock_generate_descriptions.side_effect = [
            "Pikachu description",
            "Charizard description"
        ]
        
        response = await async_client.get(f"/api/v1/pokemon/compare/{pokemon1}/{pokemon2}")
        
        assert response.status_code == 200
        expected_response = "Pikachu description\n\nCharizard description"
        assert response.json() == expected_response

    def test_strategy_endpoint_success(self, client, mock_llm):
        """Test successful strategy generation"""
        user_query = "How to beat Elite Four?"
        
        with patch('app.api.endpoints.llm', mock_llm):
            response = client.post(
                "/api/v1/pokemon/strategy",
                json=user_query
            )
            
            assert response.status_code == 200
            assert response.json() == "Mock LLM response"
            mock_llm.generate_content.assert_called_once()

    def test_strategy_endpoint_llm_error(self, client, mock_llm):
        """Test strategy endpoint with LLM error"""
        user_query = "How to beat Elite Four?"
        mock_llm.generate_content.side_effect = Exception("LLM Error")
        
        with patch('app.api.endpoints.llm', mock_llm):
            response = client.post(
                "/api/v1/pokemon/strategy",
                json=user_query
            )
            
            assert response.status_code == 500
            assert "LLM Error" in response.json()["detail"]

    def test_strategy_endpoint_empty_query(self, client, mock_llm):
        """Test strategy endpoint with empty query"""
        user_query = ""
        
        with patch('app.api.endpoints.llm', mock_llm):
            response = client.post(
                "/api/v1/pokemon/strategy",
                json=user_query
            )
            
            assert response.status_code == 200
            mock_llm.generate_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_strategy_endpoint_async(self, async_client, mock_llm):
        """Test strategy endpoint with async client"""
        user_query = "How to beat Elite Four?"
        
        with patch('app.api.endpoints.llm', mock_llm):
            response = await async_client.post(
                "/api/v1/pokemon/strategy",
                json=user_query
            )
            
            assert response.status_code == 200
            assert response.json() == "Mock LLM response"

    def test_team_building_endpoint_success(self, client, mock_llm):
        """Test successful team building"""
        user_query = "Build a balanced team for competitive play"
        
        with patch('app.api.endpoints.llm', mock_llm):
            response = client.post(
                "/api/v1/pokemon/team-building",
                json=user_query
            )
            
            assert response.status_code == 200
            assert response.json() == "Mock LLM response"
            mock_llm.generate_content.assert_called_once()

    def test_team_building_endpoint_llm_error(self, client, mock_llm):
        """Test team building endpoint with LLM error"""
        user_query = "Build a team"
        mock_llm.generate_content.side_effect = Exception("LLM Error")
        
        with patch('app.api.endpoints.llm', mock_llm):
            response = client.post(
                "/api/v1/pokemon/team-building",
                json=user_query
            )
            
            assert response.status_code == 500
            assert "LLM Error" in response.json()["detail"]

    def test_team_building_endpoint_empty_query(self, client, mock_llm):
        """Test team building endpoint with empty query"""
        user_query = ""
        
        with patch('app.api.endpoints.llm', mock_llm):
            response = client.post(
                "/api/v1/pokemon/team-building",
                json=user_query
            )
            
            assert response.status_code == 200
            mock_llm.generate_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_team_building_endpoint_async(self, async_client, mock_llm):
        """Test team building endpoint with async client"""
        user_query = "Build a balanced team"
        
        with patch('app.api.endpoints.llm', mock_llm):
            response = await async_client.post(
                "/api/v1/pokemon/team-building",
                json=user_query
            )
            
            assert response.status_code == 200
            assert response.json() == "Mock LLM response"

    def test_invalid_endpoint(self, client):
        """Test accessing invalid endpoint"""
        response = client.get("/api/v1/pokemon/invalid-endpoint")
        
        assert response.status_code == 404

    def test_wrong_http_method(self, client):
        """Test using wrong HTTP method"""
        # Strategy endpoint expects POST, but GET treats "strategy" as a Pokemon name
        response = client.get("/api/v1/pokemon/strategy")
        
        # This actually hits the Pokemon endpoint with "strategy" as the name
        # So it returns 404 for Pokemon not found, not 405 Method Not Allowed
        assert response.status_code == 404
        assert "Pokemon strategy not found" in response.json()["detail"]

    def test_malformed_json_in_post(self, client):
        """Test POST endpoint with malformed JSON"""
        response = client.post(
            "/api/v1/pokemon/strategy",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.integration 
class TestEndpointIntegration:
    """Integration tests testing multiple endpoints together"""

    def test_pokemon_to_strategy_flow(self, client, mock_parse_pokemon_data, 
                                    mock_generate_descriptions, mock_llm):
        """Test flow from getting Pokemon info to creating strategy"""
        pokemon_name = "pikachu"
        
        # First get Pokemon info
        mock_parse_pokemon_data.return_value = {"name": pokemon_name, "types": ["electric"]}
        mock_generate_descriptions.return_value = "Pikachu is an Electric-type Pokemon"
        
        pokemon_response = client.get(f"/api/v1/pokemon/{pokemon_name}")
        assert pokemon_response.status_code == 200
        
        # Then create strategy based on that Pokemon
        strategy_query = f"Create a strategy using {pokemon_name}"
        with patch('app.api.endpoints.llm', mock_llm):
            strategy_response = client.post(
                "/api/v1/pokemon/strategy",
                json=strategy_query
            )
            
            assert strategy_response.status_code == 200
            assert strategy_response.json() == "Mock LLM response"

    def test_compare_to_team_building_flow(self, client, mock_parse_pokemon_data,
                                         mock_generate_descriptions, mock_llm):
        """Test flow from comparing Pokemon to building a team"""
        pokemon1, pokemon2 = "pikachu", "charizard"
        
        # First compare Pokemon
        mock_parse_pokemon_data.side_effect = [
            {"name": pokemon1}, {"name": pokemon2}
        ]
        mock_generate_descriptions.side_effect = [
            "Pikachu description", "Charizard description"
        ]
        
        compare_response = client.get(f"/api/v1/pokemon/compare/{pokemon1}/{pokemon2}")
        assert compare_response.status_code == 200
        
        # Then build team including these Pokemon
        team_query = f"Build a team with {pokemon1} and {pokemon2}"
        with patch('app.api.endpoints.llm', mock_llm):
            team_response = client.post(
                "/api/v1/pokemon/team-building",
                json=team_query
            )
            
            assert team_response.status_code == 200
            assert team_response.json() == "Mock LLM response" 
