from sqlalchemy import Column, String, Text, ForeignKey, Integer, Numeric, Enum
from sqlalchemy.orm import relationship
from .base import DatabaseModel
import enum

class DealStatus(str, enum.Enum):
    LEAD = "lead"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class Deal(DatabaseModel):
    __tablename__ = "deals"
    
    title = Column(String(200), nullable=False)
    description = Column(Text)
    value = Column(Numeric(10, 2))
    status = Column(Enum(DealStatus), default=DealStatus.LEAD)
    notes = Column(Text)
    
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="deals")
    
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    contact = relationship("Contact")
    
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"))
    pipeline = relationship("Pipeline", back_populates="deals")
    
    stage_id = Column(Integer, ForeignKey("pipeline_stages.id"))
    stage = relationship("PipelineStage", back_populates="deals")