
from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKeyConstraint, Integer, JSON, PrimaryKeyConstraint, REAL, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import uuid
from app.db.base import Base


class Candidate(Base):
    __tablename__ = 'candidate'
    

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    status: Mapped[str] = mapped_column(String(255), server_default=text("'created'::character varying"))
    user_created: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    date_created: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    user_updated: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    date_updated: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    password: Mapped[Optional[str]] = mapped_column(String(255))
    firstname: Mapped[Optional[str]] = mapped_column(String(255))
    lastname: Mapped[Optional[str]] = mapped_column(String(255))
    verified: Mapped[Optional[bool]] = mapped_column(Boolean)
    profile_info: Mapped[Optional[dict]] = mapped_column(JSON)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    progress: Mapped[Optional[str]] = mapped_column(String(255))
    action: Mapped[Optional[str]] = mapped_column(String(255))
    custom_password_set: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    personas: Mapped[Optional[str]] = mapped_column(String(255))
    roles: Mapped[Optional[str]] = mapped_column(String(255))
    last_sent_email: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    vacancy_match: Mapped[Optional[str]] = mapped_column(String(255))
    privacy_settings: Mapped[Optional[dict]] = mapped_column(JSON)
