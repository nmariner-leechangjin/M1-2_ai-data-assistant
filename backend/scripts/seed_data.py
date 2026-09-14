"""Seed development data through a running API; never seed on import."""

import json
import os
from datetime import date, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_API_BASE_URL = "http://127.0.0.1:8000"


def seed(count: int = 100, api_base_url: str | None = None) -> int:
    if count < 100:
        raise ValueError("과제 조건에 따라 최소 100개가 필요합니다.")

    base_url = (
        api_base_url
        or os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL)
    ).rstrip("/")

    endpoint = f"{base_url}/api/data"
    start = date.today() - timedelta(days=count - 1)

    for index in range(count):
        payload = {
            "date": (start + timedelta(days=index)).isoformat(),
            "value": float(100 + index),
            "memo": "개발용 seed 데이터",
        }

        request = Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=10) as response:
                if response.status != 201:
                    raise RuntimeError(
                        f"Seed request failed: HTTP {response.status}"
                    )
        except (HTTPError, URLError) as exc:
            raise RuntimeError(
                f"Seed request failed for {endpoint}: {exc}"
            ) from exc

    return count


if __name__ == "__main__":
    print(f"{seed()}개 데이터 준비 완료")
