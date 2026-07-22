from database import SessionLocal
from db_models import AnalysisRecord
from uuid import UUID
from datetime import datetime

session = SessionLocal()

record = AnalysisRecord(
    id=UUID("00000000-0000-0000-0000-000000000001"),
    product_id=UUID("00000000-0000-0000-0000-000000000001"),
    commenter_id=UUID("00000000-0000-0000-0000-000000000001"),
    text="This is a test analysis record.",
    detected_language="en",
    processed_at=datetime(2024, 6, 1, 12, 0, 0),
    aspects={"aspect1": "value1", "aspect2": "value2"},
    keywords={"keyword1": "value1", "keyword2": "value2"},
    entities={"entity1": "value1", "entity2": "value2"},
    lexical_density=0.5,
    negation_detected=False
)

session.add(record)
session.commit()
session.refresh(record)
print(record.id)