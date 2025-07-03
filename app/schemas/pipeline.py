from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PipelineStageBase(BaseModel):
    name: str
    description: Optional[str] = None
    order: int
    probability: int = 0  # 0-100 percentage

class PipelineStageCreate(PipelineStageBase):
    pipeline_id: int

class PipelineStageUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    probability: Optional[int] = None

class PipelineStageResponse(PipelineStageBase):
    id: int
    pipeline_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True

class PipelineBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_default: bool = False

class PipelineCreate(PipelineBase):
    stages: Optional[List[PipelineStageBase]] = []

class PipelineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None

class PipelineResponse(PipelineBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool
    stages: List[PipelineStageResponse] = []
    
    class Config:
        from_attributes = True

class PipelineStatus(BaseModel):
    pipeline_id: int
    pipeline_name: str
    total_deals: int
    total_value: float
    stages: List[dict]  # Will contain stage stats
    
class PipelineStageStats(BaseModel):
    stage_id: int
    stage_name: str
    order: int
    probability: int
    deals_count: int
    total_value: float
    average_value: float