import json
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Float, Boolean, Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from database.connection import Base


def generate_uuid():
    return str(uuid.uuid4())


class Festival(Base):
    __tablename__ = "festivals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)  # e.g., "Heritage", "Folk", "Religious", "Food"
    description = Column(Text, nullable=False)
    history = Column(Text, nullable=True)
    cultural_significance = Column(Text, nullable=True)
    activities = Column(Text, nullable=True)  # Stored as JSON list string or text
    food = Column(Text, nullable=True)        # Stored as JSON list string or text
    location = Column(String(255), nullable=False)
    district = Column(String(100), nullable=False, index=True)
    state = Column(String(100), default="Karnataka")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    start_date = Column(String(10), nullable=True)  # YYYY-MM-DD
    end_date = Column(String(10), nullable=True)    # YYYY-MM-DD
    tags = Column(Text, nullable=True)              # Stored as JSON list string
    tourist_info = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    
    is_published = Column(Boolean, default=True, index=True)
    verification_status = Column(String(50), default="verified", index=True)  # verified | pending | rejected
    content_version = Column(Integer, default=1)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    translations = relationship("FestivalTranslation", back_populates="festival", cascade="all, delete-orphan")

    def get_activities_list(self) -> list[str]:
        if not self.activities:
            return []
        try:
            return json.loads(self.activities)
        except Exception:
            return [a.strip() for a in self.activities.split(",") if a.strip()]

    def get_food_list(self) -> list[str]:
        if not self.food:
            return []
        try:
            return json.loads(self.food)
        except Exception:
            return [f.strip() for f in self.food.split(",") if f.strip()]

    def get_tags_list(self) -> list[str]:
        if not self.tags:
            return []
        try:
            return json.loads(self.tags)
        except Exception:
            return [t.strip() for t in self.tags.split(",") if t.strip()]

    def to_embedding_text(self) -> str:
        """
        Dynamically constructs a comprehensive semantic text document for embedding.
        Includes all cultural, geographic, activity, and historical attributes.
        """
        activities_str = ", ".join(self.get_activities_list())
        food_str = ", ".join(self.get_food_list())
        tags_str = ", ".join(self.get_tags_list())

        parts = [
            f"Festival Name: {self.name}",
            f"Category: {self.category}",
            f"Location: {self.location}, {self.district}, {self.state}",
            f"Description: {self.description or ''}",
            f"Cultural Significance: {self.cultural_significance or ''}",
            f"History: {self.history or ''}",
            f"Activities: {activities_str}",
            f"Traditional Food & Cuisine: {food_str}",
            f"Keywords & Tags: {tags_str}",
            f"Tourist Information: {self.tourist_info or ''}"
        ]
        return "\n".join([p for p in parts if p.strip()])


class FestivalTranslation(Base):
    __tablename__ = "festival_translations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    festival_id = Column(String(36), ForeignKey("festivals.id"), nullable=False, index=True)
    language = Column(String(10), nullable=False, index=True)  # en, kn, hi
    field_name = Column(String(100), nullable=False)           # e.g., name, description, history
    translated_text = Column(Text, nullable=False)
    content_version = Column(Integer, default=1)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    festival = relationship("Festival", back_populates="translations")

    __table_args__ = (
        Index("idx_festival_lang_field", "festival_id", "language", "field_name", unique=True),
    )


class TranslationCache(Base):
    __tablename__ = "translation_cache"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cache_key = Column(String(255), nullable=False, unique=True, index=True)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    original_text_hash = Column(String(64), nullable=False)
    translated_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
