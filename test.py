from database import SessionLocal
from db_models import AnalysisRecord
from uuid import UUID

session = SessionLocal()

record = session.get(
    AnalysisRecord,
    UUID("00000000-0000-0000-0000-000000000001"),
)

if record is not None:
    session.delete(record)
    session.commit()
    print("Deleted test record")
else:
    print("Test record not found")

session.close()