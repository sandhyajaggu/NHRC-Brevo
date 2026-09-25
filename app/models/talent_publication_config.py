# app/models/talent_publication_config.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class TalentPublicationConfig(Base):
    __tablename__ = "talent_publication_config"

    id = Column(Integer, primary_key=True, index=True)

    youtube_url = Column(String(500), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )