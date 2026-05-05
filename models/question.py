"""ORM-Modell für Quizfragen."""

import json
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Question(Base):
    """Repräsentiert eine Quizfrage mit vier Antwortoptionen."""

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chapter: Mapped[str] = mapped_column(String(100), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)

    # Antwortoptionen werden als JSON-String gespeichert (z.B. '["1) Opt A", "2) Opt B"]')
    options_json: Mapped[str] = mapped_column(Text, nullable=False)

    # Korrekte Antwort als Zahl (1–4)
    correct_answer: Mapped[int] = mapped_column(Integer, nullable=False)

    @property
    def options(self) -> list[str]:
        """Gibt die Antwortoptionen als Python-Liste zurück."""
        return json.loads(self.options_json)

    @options.setter
    def options(self, value: list[str]) -> None:
        """Setzt die Antwortoptionen aus einer Python-Liste."""
        self.options_json = json.dumps(value, ensure_ascii=False)

    def __repr__(self) -> str:
        return f"<Question(id={self.id}, chapter='{self.chapter}')>"