from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    POKEMON_API_URL: str = "https://pokeapi.co/api/v2"
    GEMINI_API_KEY: str = "..."



    class Config:
        case_sensitive = True
        env_file = ".env"
    
settings = Settings()
