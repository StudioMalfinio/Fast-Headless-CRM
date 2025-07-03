from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..schemas.deal import DealCreate, DealUpdate, DealResponse
from ..crud import deal as deal_crud
from ..core.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[DealResponse])
def read_deals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    deals = deal_crud.get_deals(db, skip=skip, limit=limit)
    return deals

@router.post("/", response_model=DealResponse)
def create_deal(deal: DealCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return deal_crud.create_deal(db=db, deal=deal)

@router.get("/{deal_id}", response_model=DealResponse)
def read_deal(deal_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_deal = deal_crud.get_deal(db, deal_id=deal_id)
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return db_deal

@router.put("/{deal_id}", response_model=DealResponse)
def update_deal(deal_id: int, deal: DealUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_deal = deal_crud.update_deal(db, deal_id=deal_id, deal=deal)
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return db_deal

@router.delete("/{deal_id}", response_model=DealResponse)
def delete_deal(deal_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_deal = deal_crud.delete_deal(db, deal_id=deal_id)
    if db_deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return db_deal