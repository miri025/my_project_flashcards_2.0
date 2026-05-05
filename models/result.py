"""ORM-Modell für Quiz-Ergebnisse."""

from datetime import datetime
from sqlalchemy import Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Result(Base):
    """Repräsentiert das Ergebnis einer Quiz-Session."""

    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Fremdschlüssel auf den User
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)

    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    aborted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False)
    played_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    # Beziehung zurück zum User
    user: Mapped["User"] = relationship("User", back_populates="results")

    @property
    def percentage(self) -> float:
        """Berechnet die Trefferquote in Prozent."""
        if self.total == 0:
            return 0.0
        return round(self.score / self.total * 100, 1)

    def __repr__(self) -> str:
        return (
            f"<Result(id={self.id}, user_id={self.user_id}, "
            f"score={self.score}/{self.total})>"
        )