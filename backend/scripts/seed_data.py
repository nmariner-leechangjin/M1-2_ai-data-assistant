"""Seed development data only when called as a script; never on import."""
from datetime import date, timedelta
from app.main import data_service
from app.schemas.data import DataWrite

def seed(count: int = 100) -> int:
    if count < 100: raise ValueError("과제 조건에 따라 최소 100개가 필요합니다.")
    start = date.today() - timedelta(days=count - 1)
    for index in range(count):
        data_service.create(DataWrite(date=start + timedelta(days=index), value=float(100 + index), memo="개발용 seed 데이터"))
    return count

if __name__ == "__main__": print(f"{seed()}개 데이터 준비 완료")
