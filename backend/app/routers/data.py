from fastapi import APIRouter, Depends
from app.schemas.data import DataOut, DataWrite, SummaryOut
router = APIRouter(prefix="/api/data", tags=["data"])
def service(): from app.main import data_service; return data_service
@router.post("", response_model=DataOut, status_code=201)
def create(item: DataWrite, svc=Depends(service)): return svc.create(item)
@router.get("", response_model=list[DataOut])
def list_all(svc=Depends(service)): return svc.list()
@router.get("/summary", response_model=SummaryOut)
def summary(svc=Depends(service)): return svc.summary()
@router.put("/{item_id}", response_model=DataOut)
def update(item_id: str, item: DataWrite, svc=Depends(service)): return svc.update(item_id, item)
@router.delete("/{item_id}")
def delete(item_id: str, svc=Depends(service)): svc.delete(item_id); return {"deleted":True}
