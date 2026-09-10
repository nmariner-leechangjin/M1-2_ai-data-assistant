import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    use_mock_services: bool
    openai_api_key: str | None
    openai_model: str
    firebase_service_account_json: str | None
    allowed_origins: list[str]

def get_settings() -> Settings:
    origins = [item.strip() for item in os.getenv("ALLOWED_ORIGINS", "http://localhost:5500").split(",") if item.strip()]
    return Settings(os.getenv("USE_MOCK_SERVICES", "false").lower() == "true", os.getenv("OPENAI_API_KEY") or None, os.getenv("OPENAI_MODEL", "gpt-4o-mini"), os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON") or None, origins)
