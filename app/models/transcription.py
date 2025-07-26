from sqlalchemy import Column, String, DateTime, Text, Integer
from app.config.database import Base
import uuid
from datetime import datetime


class ConvertedSound(Base):
    __tablename__ = "converted_sounds"

    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    talent_id = Column(String(50), nullable=False, index=True)
    acc_id = Column(String(50), nullable=False, index=True)
    text = Column(Text, nullable=True)
    encoded_text = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="pending", index=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "uuid": str(self.uuid),
            "talent_id": self.talent_id,
            "acc_id": self.acc_id,
            "text": self.text,
            "status": self.status,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
