# Test Suite Documentation

This directory contains focused unit and integration tests for the Pokebase backend API endpoints and Pokemon service.

## Test Structure

### Test Files

- **`conftest.py`** - Shared test fixtures and configuration
- **`test_pokemon_service.py`** - Unit tests for Pokemon service layer
- **`test_api_endpoints.py`** - Integration tests for all API endpoints

### Test Categories

Tests are marked with pytest markers:

- `@pytest.mark.unit` - Unit tests for individual components
- `@pytest.mark.integration` - Integration tests for API endpoints

## Running Tests

### Run All Tests
```bash
pdm run test
```

### Run Specific Test Categories
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Run Specific Test Files
```bash
# Run service tests
pytest tests/test_pokemon_service.py

# Run API endpoint tests
pytest tests/test_api_endpoints.py

# Run with verbose output
pytest tests/ -v
```

### Run Tests with Coverage
```bash
pytest --cov=app tests/
```

## Test Coverage

The test suite covers:

### Unit Tests
- **Pokemon Service** (`PokemonService`)
  - Data fetching from external Pokemon API
  - Error handling (404, network errors, JSON parsing)
  - Concurrent request handling
  - Special character handling in Pokemon names

### Integration Tests
- **API Endpoints**
  - Health check endpoint (`/api/v1/health`)
  - Pokemon retrieval (`/api/v1/pokemon/{name}`)
  - Pokemon comparison (`/api/v1/pokemon/compare/{name1}/{name2}`)
  - Strategy generation (`/api/v1/pokemon/strategy`)
  - Team building (`/api/v1/pokemon/team-building`)
  - Error handling and HTTP status codes
  - Concurrent request handling

## Test Fixtures

### Data Fixtures
- `sample_pokemon_data` - Mock Pokemon API response data
- `test_settings` - Test configuration settings

### Client Fixtures
- `client` - Synchronous FastAPI test client
- `async_client` - Asynchronous FastAPI test client

### Mock Fixtures
- `mock_llm` - Mock LLM service for strategy/team generation endpoints
- `mock_aiohttp_session` - Mock aiohttp session for Pokemon service
- `mock_parse_pokemon_data` - Mock Pokemon data parsing function
- `mock_generate_descriptions` - Mock description generation function

## Mocking Strategy

The tests use comprehensive mocking to:

1. **Isolate Components** - Each test focuses on a single component
2. **Avoid External Dependencies** - Mock external APIs and services
3. **Control Test Data** - Use predictable test data
4. **Speed Up Tests** - Avoid real network calls

### Key Mocks
- External Pokemon API calls (`aiohttp.ClientSession`)
- LLM service calls (`google.genai`)
- Pokemon data parsing and description generation

## Best Practices

1. **Test Isolation** - Each test is independent and can run in any order
2. **Descriptive Names** - Test names clearly describe what is being tested
3. **Arrange-Act-Assert** - Tests follow the AAA pattern
4. **Error Cases** - Both success and failure scenarios are tested
5. **Edge Cases** - Special characters, empty data, concurrent requests

## Adding New Tests

When adding new functionality:

1. **Add Unit Tests** - Test individual functions/classes in isolation
2. **Add Integration Tests** - Test API endpoints and workflows
3. **Update Fixtures** - Add new test data as needed
4. **Mock External Dependencies** - Keep tests fast and reliable
5. **Use Appropriate Markers** - Mark tests as unit/integration

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

- Fast execution (mocked external dependencies)
- Reliable (no flaky network calls)
- Comprehensive coverage for core functionality
- Clear failure reporting 
