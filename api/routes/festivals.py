import json
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Festival
from ai.recommendation.index_manager import IndexManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/festivals", tags=["Festival Database & Publishing Workflow"])


class FestivalCreateInput(BaseModel):
    name: str
    category: str
    description: str
    history: Optional[str] = None
    cultural_significance: Optional[str] = None
    activities: List[str] = Field(default_factory=list)
    food: List[str] = Field(default_factory=list)
    location: str
    district: str
    state: str = "Karnataka"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    start_date: Optional[str] = None  # YYYY-MM-DD
    end_date: Optional[str] = None    # YYYY-MM-DD
    tags: List[str] = Field(default_factory=list)
    tourist_info: Optional[str] = None
    image_url: Optional[str] = None
    is_published: bool = True
    verification_status: str = "verified"


@router.get("", summary="List Published Festivals")
def list_festivals(
    published_only: bool = True,
    category: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Festival)
    if published_only:
        query = query.filter(Festival.is_published == True, Festival.verification_status == "verified")
    if category:
        query = query.filter(Festival.category.ilike(f"%{category}%"))
    if district:
        query = query.filter(Festival.district.ilike(f"%{district}%"))

    festivals = query.all()
    return {
        "count": len(festivals),
        "festivals": [
            {
                "id": f.id,
                "name": f.name,
                "category": f.category,
                "description": f.description,
                "location": f.location,
                "district": f.district,
                "latitude": f.latitude,
                "longitude": f.longitude,
                "start_date": f.start_date,
                "end_date": f.end_date,
                "activities": f.get_activities_list(),
                "food": f.get_food_list(),
                "tags": f.get_tags_list(),
                "is_published": f.is_published,
                "verification_status": f.verification_status,
                "image_url": f.image_url
            }
            for f in festivals
        ]
    }


@router.get("/{festival_id}", summary="Get Festival Details by ID")
def get_festival(festival_id: str, db: Session = Depends(get_db)):
    fest = db.query(Festival).filter(Festival.id == festival_id).first()
    if not fest:
        raise HTTPException(status_code=404, detail="Festival not found.")
    return {
        "id": fest.id,
        "name": fest.name,
        "category": fest.category,
        "description": fest.description,
        "history": fest.history,
        "cultural_significance": fest.cultural_significance,
        "activities": fest.get_activities_list(),
        "food": fest.get_food_list(),
        "location": fest.location,
        "district": fest.district,
        "state": fest.state,
        "latitude": fest.latitude,
        "longitude": fest.longitude,
        "start_date": fest.start_date,
        "end_date": fest.end_date,
        "tags": fest.get_tags_list(),
        "tourist_info": fest.tourist_info,
        "image_url": fest.image_url,
        "is_published": fest.is_published,
        "verification_status": fest.verification_status,
        "updated_at": fest.updated_at.isoformat() if fest.updated_at else None
    }


@router.post("", summary="Publish New Festival & Trigger AI Indexing", status_code=201)
def create_festival(data: FestivalCreateInput, db: Session = Depends(get_db)):
    fest = Festival(
        name=data.name,
        category=data.category,
        description=data.description,
        history=data.history,
        cultural_significance=data.cultural_significance,
        activities=json.dumps(data.activities),
        food=json.dumps(data.food),
        location=data.location,
        district=data.district,
        state=data.state,
        latitude=data.latitude,
        longitude=data.longitude,
        start_date=data.start_date,
        end_date=data.end_date,
        tags=json.dumps(data.tags),
        tourist_info=data.tourist_info,
        image_url=data.image_url,
        is_published=data.is_published,
        verification_status=data.verification_status
    )
    db.add(fest)
    db.commit()
    db.refresh(fest)

    # Trigger automatic indexing in FAISS vector store
    manager = IndexManager(db)
    indexed = manager.index_festival(fest.id)

    return {
        "success": True,
        "message": f"Festival '{fest.name}' created and indexed successfully.",
        "festival_id": fest.id,
        "ai_indexed": indexed
    }


@router.put("/{festival_id}/publish-status", summary="Update Publish/Verification Status")
def update_publish_status(
    festival_id: str,
    is_published: bool,
    verification_status: str = "verified",
    db: Session = Depends(get_db)
):
    fest = db.query(Festival).filter(Festival.id == festival_id).first()
    if not fest:
        raise HTTPException(status_code=404, detail="Festival not found.")

    fest.is_published = is_published
    fest.verification_status = verification_status
    db.commit()

    # Trigger FAISS index update / vector removal if unpublished
    manager = IndexManager(db)
    indexed = manager.index_festival(fest.id)

    return {
        "success": True,
        "festival_id": fest.id,
        "is_published": fest.is_published,
        "verification_status": fest.verification_status,
        "ai_indexed": indexed
    }
