from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from ..models.pipeline import Pipeline, PipelineStage
from ..models.deal import Deal
from ..schemas.pipeline import PipelineCreate, PipelineUpdate, PipelineStageCreate, PipelineStageUpdate

def get_pipeline(db: Session, pipeline_id: int) -> Optional[Pipeline]:
    return db.query(Pipeline).filter(and_(Pipeline.id == pipeline_id, Pipeline.is_active == True)).first()

def get_pipelines(db: Session, skip: int = 0, limit: int = 100) -> List[Pipeline]:
    return db.query(Pipeline).filter(Pipeline.is_active == True).offset(skip).limit(limit).all()

def create_pipeline(db: Session, pipeline: PipelineCreate) -> Pipeline:
    db_pipeline = Pipeline(
        name=pipeline.name,
        description=pipeline.description,
        is_default=pipeline.is_default
    )
    db.add(db_pipeline)
    db.commit()
    db.refresh(db_pipeline)
    
    # Create stages if provided
    for i, stage_data in enumerate(pipeline.stages):
        stage = PipelineStage(
            name=stage_data.name,
            description=stage_data.description,
            order=stage_data.order if stage_data.order else i + 1,
            probability=stage_data.probability,
            pipeline_id=db_pipeline.id
        )
        db.add(stage)
    
    if pipeline.stages:
        db.commit()
        db.refresh(db_pipeline)
    
    return db_pipeline

def update_pipeline(db: Session, pipeline_id: int, pipeline: PipelineUpdate) -> Optional[Pipeline]:
    db_pipeline = get_pipeline(db, pipeline_id)
    if db_pipeline:
        update_data = pipeline.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_pipeline, field, value)
        db.commit()
        db.refresh(db_pipeline)
    return db_pipeline

def delete_pipeline(db: Session, pipeline_id: int) -> Optional[Pipeline]:
    db_pipeline = get_pipeline(db, pipeline_id)
    if db_pipeline:
        db_pipeline.is_active = False
        db.commit()
        db.refresh(db_pipeline)
    return db_pipeline

def get_pipeline_stage(db: Session, stage_id: int) -> Optional[PipelineStage]:
    return db.query(PipelineStage).filter(and_(PipelineStage.id == stage_id, PipelineStage.is_active == True)).first()

def create_pipeline_stage(db: Session, stage: PipelineStageCreate) -> PipelineStage:
    db_stage = PipelineStage(**stage.dict())
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage

def update_pipeline_stage(db: Session, stage_id: int, stage: PipelineStageUpdate) -> Optional[PipelineStage]:
    db_stage = get_pipeline_stage(db, stage_id)
    if db_stage:
        update_data = stage.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_stage, field, value)
        db.commit()
        db.refresh(db_stage)
    return db_stage

def get_pipeline_status(db: Session, pipeline_id: int) -> dict:
    """Get comprehensive pipeline status with deal statistics"""
    pipeline = get_pipeline(db, pipeline_id)
    if not pipeline:
        return None
    
    # Get stages with deal counts and values
    stage_stats = db.query(
        PipelineStage.id,
        PipelineStage.name,
        PipelineStage.order,
        PipelineStage.probability,
        func.count(Deal.id).label('deals_count'),
        func.coalesce(func.sum(Deal.value), 0).label('total_value')
    ).outerjoin(
        Deal, and_(Deal.stage_id == PipelineStage.id, Deal.is_active == True)
    ).filter(
        and_(PipelineStage.pipeline_id == pipeline_id, PipelineStage.is_active == True)
    ).group_by(
        PipelineStage.id, PipelineStage.name, PipelineStage.order, PipelineStage.probability
    ).order_by(PipelineStage.order).all()
    
    # Get total pipeline stats
    total_deals = db.query(func.count(Deal.id)).filter(
        and_(Deal.pipeline_id == pipeline_id, Deal.is_active == True)
    ).scalar() or 0
    
    total_value = db.query(func.coalesce(func.sum(Deal.value), 0)).filter(
        and_(Deal.pipeline_id == pipeline_id, Deal.is_active == True)
    ).scalar() or 0
    
    stages_data = []
    for stage in stage_stats:
        avg_value = float(stage.total_value) / stage.deals_count if stage.deals_count > 0 else 0
        stages_data.append({
            "stage_id": stage.id,
            "stage_name": stage.name,
            "order": stage.order,
            "probability": stage.probability,
            "deals_count": stage.deals_count,
            "total_value": float(stage.total_value),
            "average_value": avg_value
        })
    
    return {
        "pipeline_id": pipeline.id,
        "pipeline_name": pipeline.name,
        "total_deals": total_deals,
        "total_value": float(total_value),
        "stages": stages_data
    }