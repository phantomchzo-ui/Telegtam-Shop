from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TG_TOKEN: str
    API_KEY_CURRENCY: str
    API_KEY_WEATHER: str

    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

