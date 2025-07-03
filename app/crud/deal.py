from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from ..models.deal import Deal
from ..schemas.deal import DealCreate, DealUpdate

def get_deal(db: Session, deal_id: int) -> Optional[Deal]:
    return db.query(Deal).filter(and_(Deal.id == deal_id, Deal.is_active == True)).first()

def get_deals(db: Session, skip: int = 0, limit: int = 100) -> List[Deal]:
    return db.query(Deal).filter(Deal.is_active == True).offset(skip).limit(limit).all()

def create_deal(db: Session, deal: DealCreate) -> Deal:
    db_deal = Deal(**deal.dict())
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal

def update_deal(db: Session, deal_id: int, deal: DealUpdate) -> Optional[Deal]:
    db_deal = get_deal(db, deal_id)
    if db_deal:
        update_data = deal.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_deal, field, value)
        db.commit()
        db.refresh(db_deal)
    return db_deal

def delete_deal(db: Session, deal_id: int) -> Optional[Deal]:
    db_deal = get_deal(db, deal_id)
    if db_deal:
        db_deal.is_active = False
        db.commit()
        db.refresh(db_deal)
    return db_deal