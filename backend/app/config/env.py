from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    POKEMON_API_URL: str = "https://pokeapi.co/api/v2/"



    class Config:
        case_sensitive = True
        env_file = ".env"
    
settings = Settings()
