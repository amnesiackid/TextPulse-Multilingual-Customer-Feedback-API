from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Float, Boolean, DateTime
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.dialects.postgresql import JSONB
from uuid import UUID
from datetime import datetime

class AnalysisRecord(Base):
    __tablename__ = "analyses"

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True)
    product_name: Mapped[str] = mapped_column(Text, nullable=False)
    product_id: Mapped[UUID] = mapped_column(SQLUUID, nullable=False)
    commenter_id: Mapped[UUID] = mapped_column(SQLUUID, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    detected_language: Mapped[str] = mapped_column(Text, nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    aspects: Mapped[dict] = mapped_column(JSONB, nullable=False)
    keywords: Mapped[dict] = mapped_column(JSONB, nullable=False)
    entities: Mapped[dict] = mapped_column(JSONB, nullable=False)
    lexical_density: Mapped[float] = mapped_column(Float, nullable=False)
    negation_detected: Mapped[bool] = mapped_column(Boolean, nullable=False)
    