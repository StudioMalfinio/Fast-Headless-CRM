from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from ..models.contact import Contact
from ..schemas.contact import ContactCreate, ContactUpdate

def get_contact(db: Session, contact_id: int) -> Optional[Contact]:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.is_active == True)).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
    return db.query(Contact).filter(Contact.is_active == True).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactUpdate) -> Optional[Contact]:
    db_contact = get_contact(db, contact_id)
    if db_contact:
        update_data = contact.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int) -> Optional[Contact]:
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db_contact.is_active = False
        db.commit()
        db.refresh(db_contact)
    return db_contact