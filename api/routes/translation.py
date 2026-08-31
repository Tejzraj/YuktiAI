import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from ai.models.schemas import (
    TranslationRequest,
    TranslationResponse,
    BatchTranslationRequest,
    BatchTranslationResponse,
    FestivalTranslationResponse
)
from ai.translation.translation_service import TranslationService
from ai.translation.language_detector import detect_language

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Multilingual Subsystem"])


@router.post(
    "/translate",
    response_model=TranslationResponse,
    summary="Translate Single Text String",
    description="Translates a text string between English, Kannada, and Hindi with caching and fallbacks."
)
def translate_single_text(
    request: TranslationRequest,
    db: Session = Depends(get_db)
):
    try:
        service = TranslationService(db)
        src_lang = request.source_language or detect_language(request.text)
        translated = service.translate_text(
            text=request.text,
            target_language=request.target_language,
            source_language=src_lang
        )
        return TranslationResponse(
            success=True,
            source_language=src_lang,
            target_language=request.target_language,
            translated_text=translated
        )
    except Exception as e:
        logger.error(f"Translation API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )


@router.post(
    "/translate/batch",
    response_model=BatchTranslationResponse,
    summary="Batch Translate List of Texts",
    description="Batch translates multiple text strings efficiently using persistent cache."
)
def translate_batch_texts(
    request: BatchTranslationRequest,
    db: Session = Depends(get_db)
):
    try:
        service = TranslationService(db)
        src_lang = request.source_language or (detect_language(request.texts[0]) if request.texts else "en")
        translated_list = service.translate_batch(
            texts=request.texts,
            target_language=request.target_language,
            source_language=src_lang
        )
        return BatchTranslationResponse(
            success=True,
            source_language=src_lang,
            target_language=request.target_language,
            translated_texts=translated_list
        )
    except Exception as e:
        logger.error(f"Batch translation API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch translation failed: {str(e)}"
        )


@router.post(
    "/festivals/{festival_id}/translate",
    response_model=FestivalTranslationResponse,
    summary="Translate Structured Festival Content",
    description="Returns translated structured fields (name, description, activities, food, cultural significance) for a festival without altering original DB data."
)
def translate_festival_content(
    festival_id: str,
    target_language: str,
    db: Session = Depends(get_db)
):
    try:
        service = TranslationService(db)
        return service.translate_festival_fields(festival_id, target_language)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        logger.error(f"Festival content translation API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Festival content translation failed: {str(e)}"
        )
