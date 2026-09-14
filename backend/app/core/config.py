import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    use_mock_services: bool
    openai_api_key: str
    openai_model: str
    openai_base_url: str
    firebase_service_account_json: str
    allowed_origins: list[str]


def get_settings() -> Settings:
    use_mock_services = os.getenv("USE_MOCK_SERVICES", "false").lower() == "true"

    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    openai_model = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
    openai_base_url = os.getenv("OPENAI_BASE_URL", "")

    firebase_service_account_json = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_JSON",
        ""
    )

    allowed_origins_raw = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5500,http://127.0.0.1:5500"
    )

    allowed_origins = [
        origin.strip()
        for origin in allowed_origins_raw.split(",")
        if origin.strip()
    ]

    return Settings(
        use_mock_services=use_mock_services,
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        openai_base_url=openai_base_url,
        firebase_service_account_json=firebase_service_account_json,
        allowed_origins=allowed_origins,
    )