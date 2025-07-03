from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..schemas.pipeline import (
    PipelineCreate, PipelineUpdate, PipelineResponse, PipelineStatus,
    PipelineStageCreate, PipelineStageUpdate, PipelineStageResponse
)
from ..crud import pipeline as pipeline_crud
from ..core.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PipelineResponse])
def read_pipelines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    pipelines = pipeline_crud.get_pipelines(db, skip=skip, limit=limit)
    return pipelines

@router.post("/", response_model=PipelineResponse)
def create_pipeline(pipeline: PipelineCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return pipeline_crud.create_pipeline(db=db, pipeline=pipeline)

@router.get("/{pipeline_id}", response_model=PipelineResponse)
def read_pipeline(pipeline_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_pipeline = pipeline_crud.get_pipeline(db, pipeline_id=pipeline_id)
    if db_pipeline is None:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return db_pipeline

@router.put("/{pipeline_id}", response_model=PipelineResponse)
def update_pipeline(pipeline_id: int, pipeline: PipelineUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_pipeline = pipeline_crud.update_pipeline(db, pipeline_id=pipeline_id, pipeline=pipeline)
    if db_pipeline is None:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return db_pipeline

@router.delete("/{pipeline_id}", response_model=PipelineResponse)
def delete_pipeline(pipeline_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_pipeline = pipeline_crud.delete_pipeline(db, pipeline_id=pipeline_id)
    if db_pipeline is None:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return db_pipeline

@router.get("/{pipeline_id}/status")
def get_pipeline_status(pipeline_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Get comprehensive pipeline status with deal statistics"""
    status = pipeline_crud.get_pipeline_status(db, pipeline_id=pipeline_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return status

@router.post("/{pipeline_id}/stages", response_model=PipelineStageResponse)
def create_pipeline_stage(pipeline_id: int, stage: PipelineStageCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Verify pipeline exists
    if not pipeline_crud.get_pipeline(db, pipeline_id):
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    stage.pipeline_id = pipeline_id
    return pipeline_crud.create_pipeline_stage(db=db, stage=stage)

@router.put("/stages/{stage_id}", response_model=PipelineStageResponse)
def update_pipeline_stage(stage_id: int, stage: PipelineStageUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_stage = pipeline_crud.update_pipeline_stage(db, stage_id=stage_id, stage=stage)
    if db_stage is None:
        raise HTTPException(status_code=404, detail="Pipeline stage not found")
    return db_stage