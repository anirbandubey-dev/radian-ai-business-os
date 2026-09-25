from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://radian:radian@localhost:5432/radian"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "development-only-secret"
    cors_origins: list[str] = ["http://localhost:3000"]
    clerk_jwt_issuer: str = ""
    clerk_jwks_url: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

