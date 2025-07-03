from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import DatabaseModel

class Company(DatabaseModel):
    __tablename__ = "companies"
    
    name = Column(String(200), nullable=False)
    website = Column(String(255))
    industry = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    notes = Column(Text)
    
    contacts = relationship("Contact", back_populates="company")
    deals = relationship("Deal", back_populates="company")