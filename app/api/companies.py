from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from ..crud import company as company_crud
from ..core.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CompanyResponse])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    companies = company_crud.get_companies(db, skip=skip, limit=limit)
    return companies

@router.post("/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return company_crud.create_company(db=db, company=company)

@router.get("/{company_id}", response_model=CompanyResponse)
def read_company(company_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_company = company_crud.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_company = company_crud.update_company(db, company_id=company_id, company=company)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.delete("/{company_id}", response_model=CompanyResponse)
def delete_company(company_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_company = company_crud.delete_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company