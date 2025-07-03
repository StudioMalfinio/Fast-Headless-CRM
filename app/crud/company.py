from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from ..models.company import Company
from ..schemas.company import CompanyCreate, CompanyUpdate

def get_company(db: Session, company_id: int) -> Optional[Company]:
    return db.query(Company).filter(and_(Company.id == company_id, Company.is_active == True)).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100) -> List[Company]:
    return db.query(Company).filter(Company.is_active == True).offset(skip).limit(limit).all()

def create_company(db: Session, company: CompanyCreate) -> Company:
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company: CompanyUpdate) -> Optional[Company]:
    db_company = get_company(db, company_id)
    if db_company:
        update_data = company.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_company, field, value)
        db.commit()
        db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int) -> Optional[Company]:
    db_company = get_company(db, company_id)
    if db_company:
        db_company.is_active = False
        db.commit()
        db.refresh(db_company)
    return db_company