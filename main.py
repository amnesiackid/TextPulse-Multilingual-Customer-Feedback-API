import spacy
import models
from dependencies import get_settings, get_nlp
from fastapi import FastAPI, HTTPException, Depends, Request
from contextlib import asynccontextmanager
from datetime import datetime 
from nlp_utils import extract_keywords, extract_entities, extract_linguistic_metrics

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
async def analyze(request: models.AnalysisRequest, settings: dict = Depends(get_settings), nlp = Depends(get_nlp)) -> models.AnalysisResponse:
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
    entities = extract_entities(doc)
    metrics = extract_linguistic_metrics(doc)
    return models.AnalysisResponse(
        product_id=request.product_id,
        commenter_id=request.commenter_id,
        detected_language=detected_language,
        processed_at=datetime.now(),
        aspects=[models.AspectResult(aspect="delivery", polarity=0.5, excerpt="The DHL delivery was quick and efficient.")],
        keywords=keywords,
        entities=entities,
        metrics=models.LinguisticMetrics(lexical_density=metrics["lexical_density"], negation_detected=metrics["negation_detected"])
    )