from datetime import datetime
from typing import Literal, Optional
from uuid import UUID
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    text: str
    language_hint: Optional[Literal["en", "fr", "it", "de"]] = None
    product_id: UUID
    commenter_id: UUID

class AspectResult(BaseModel):
    aspect: str
    polarity: float = Field(ge=-1.0, le=1.0)
    excerpt: str

class EntityResult(BaseModel):
    text: str
    label: str

class LinguisticMetrics(BaseModel):
    lexical_density: float
    negation_detected: bool

class AnalysisResponse(BaseModel):
    product_id: UUID
    commenter_id: UUID
    detected_language:Literal["en", "fr", "it", "de"]
    processed_at: datetime
    aspects: list[AspectResult]
    keywords: list[str]
    entities: list[EntityResult]
    metrics: LinguisticMetrics
    
    