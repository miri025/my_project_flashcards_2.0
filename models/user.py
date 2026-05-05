"""ORM-Modell für Benutzer."""

from datetime import datetime
from models.result import Result
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class User(Base):
    """Repräsentiert einen registrierten Benutzer."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    # Beziehung: Ein User hat mehrere Ergebnisse
    results: Mapped[list["Result"]] = relationship(
        "Result", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"