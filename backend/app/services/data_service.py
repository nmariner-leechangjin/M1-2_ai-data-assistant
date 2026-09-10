from fastapi import HTTPException
class DataService:
    def __init__(self, repository): self.repository = repository
    def create(self, item): return self.repository.create_data(item.model_dump(mode="json"))
    def list(self): return sorted(self.repository.list_data(), key=lambda row: row["date"])
    def update(self, item_id, item):
        row = self.repository.update_data(item_id, item.model_dump(mode="json"))
        if not row: raise HTTPException(404, "데이터를 찾을 수 없습니다.")
        return row
    def delete(self, item_id):
        if not self.repository.delete_data(item_id): raise HTTPException(404, "데이터를 찾을 수 없습니다.")
    def summary(self):
        rows = self.list()
        if not rows: return {"period_start":None,"period_end":None,"count":0,"average":None,"minimum":None,"maximum":None,"recent_trend":"데이터 없음"}
        values, recent = [row["value"] for row in rows], rows[-7:]
        trend = "상승" if recent[-1]["value"] > recent[0]["value"] else "하락" if recent[-1]["value"] < recent[0]["value"] else "보합"
        return {"period_start":rows[0]["date"],"period_end":rows[-1]["date"],"count":len(rows),"average":round(sum(values)/len(values),2),"minimum":min(values),"maximum":max(values),"recent_trend":trend}
