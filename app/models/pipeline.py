from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import DatabaseModel

class Pipeline(DatabaseModel):
    __tablename__ = "pipelines"
    
    name = Column(String(200), nullable=False)
    description = Column(Text)
    is_default = Column(Boolean, default=False)
    
    stages = relationship("PipelineStage", back_populates="pipeline", cascade="all, delete-orphan")
    deals = relationship("Deal", back_populates="pipeline")

class PipelineStage(DatabaseModel):
    __tablename__ = "pipeline_stages"
    
    name = Column(String(200), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)
    probability = Column(Integer, default=0)  # Win probability percentage (0-100)
    
    pipeline_id = Column(Integer, ForeignKey("pipelines.id"), nullable=False)
    pipeline = relationship("Pipeline", back_populates="stages")
    
    deals = relationship("Deal", back_populates="stage")