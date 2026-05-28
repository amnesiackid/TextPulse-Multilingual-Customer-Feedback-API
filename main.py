import models
from fastapi import FastAPI
from datetime import datetime 
app = FastAPI()

    
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/analyze")
async def analyze(request: models.AnalysisRequest) -> models.AnalysisResponse:
    return models.AnalysisResponse(
        product_id=request.product_id,
        commenter_id=request.commenter_id,
        detected_language=request.language_hint or "en",
        processed_at=datetime.now(),
        aspects=[models.AspectResult(aspect="delivery", polarity=0.5, excerpt="The DHL delivery was quick and efficient.")],
        keywords=["delivery", "quick", "efficient"],
        entities=[models.EntityResult(text="DHL", label="ORG")],
        metrics=models.LinguisticMetrics(lexical_density=0.0, negation_detected=False)
    )