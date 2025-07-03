from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from ..models.deal import DealStatus

class DealBase(BaseModel):
    title: str
    description: Optional[str] = None
    value: Optional[Decimal] = None
    status: DealStatus = DealStatus.LEAD
    notes: Optional[str] = None
    company_id: Optional[int] = None
    contact_id: Optional[int] = None

class DealCreate(DealBase):
    pass

class DealUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    value: Optional[Decimal] = None
    status: Optional[DealStatus] = None
    notes: Optional[str] = None
    company_id: Optional[int] = None
    contact_id: Optional[int] = None

class DealResponse(DealBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True