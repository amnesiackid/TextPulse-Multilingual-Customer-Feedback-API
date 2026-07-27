import spacy
import models, db_models
from dependencies import get_settings, get_nlp, get_db
from fastapi import FastAPI, HTTPException, Depends, Request
from contextlib import asynccontextmanager
from datetime import datetime 
from nlp_utils import extract_keywords, extract_aspects, extract_entities, extract_linguistic_metrics
from sqlalchemy.orm import Session
from db_models import AnalysisRecord
from uuid import uuid4

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup: runs once before the first request ---
    print("TextPulse starting up")
    app.state.nlp = spacy.load("en_core_web_sm")
    yield
    # --- shutdown: runs once after the last request ---
    print("TextPulse is shutting down")

app = FastAPI(lifespan=lifespan)



@app.get("/health")
async def health_check(settings: dict = Depends(get_settings)):
    return {"status": "ok", "version": settings["app_version"]}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/analyze")
async def analyze(request: models.AnalysisRequest, settings: dict = Depends(get_settings), nlp = Depends(get_nlp), db: Session = Depends(get_db)) -> models.AnalysisResponse:
    text = request.text
    # validation checks
    if not any(c.isalpha() for c in text):
        raise HTTPException(status_code=422, detail="Text must contain at least one alphabetic character")
    text_word_count = len(text.split())
    if text_word_count < settings["min_word_count"]:
        raise HTTPException(status_code=422, detail=f"Text must contain at least {settings['min_word_count']} words")
    if text_word_count > settings["max_word_count"]:
        raise HTTPException(status_code=422, detail=f"Text must not exceed {settings['max_word_count']} words")
    doc = nlp(text)
    
    # hardcoded now
    detected_language = "en"
    keywords = extract_keywords(doc)
    aspects = extract_aspects(doc)
    entities = extract_entities(doc)
    metrics = extract_linguistic_metrics(doc)
    processed_at = datetime.now()
    record = db_models.AnalysisRecord(
            id=uuid4(),
            product_id=request.product_id,
            commenter_id=request.commenter_id,
            text=text,
            detected_language=detected_language,
            processed_at=processed_at,
            aspects=[aspect.model_dump() for aspect in aspects],
            keywords=keywords,
            entities=[entity.model_dump() for entity in entities],
            lexical_density=metrics.lexical_density,
            negation_detected=metrics.negation_detected
        )
    db.add(record)
    db.commit()
    db.refresh(record)
    return models.AnalysisResponse(
        product_id=request.product_id,
        commenter_id=request.commenter_id,
        detected_language=detected_language,
        processed_at=processed_at,
        aspects=aspects,
        keywords=keywords,
        entities=entities,
        metrics=metrics
    )
    