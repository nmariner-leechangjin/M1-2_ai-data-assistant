from datetime import date
from pydantic import BaseModel, Field
class DataWrite(BaseModel):
    date: date
    value: float
    memo: str = Field(default="", max_length=500)
class DataOut(DataWrite): id: str
class SummaryOut(BaseModel):
    period_start: str | None; period_end: str | None; count: int; average: float | None; minimum: float | None; maximum: float | None; recent_trend: str
