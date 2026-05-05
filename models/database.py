"""Datenbank-Initialisierung und Session-Verwaltung."""

import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.base import Base
from models.user import User
from models.question import Question
from models.result import Result

# SQLite-Datenbankdatei im Projektroot
DATABASE_URL = "sqlite:///flashcards.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db() -> None:
    """
    Erstellt alle Tabellen und befüllt die Datenbank mit Seed-Daten,
    falls noch keine Fragen vorhanden sind.
    """
    Base.metadata.create_all(bind=engine)
    _seed_questions()


def get_session() -> Session:
    """Gibt eine neue Datenbank-Session zurück."""
    return SessionLocal()


def _seed_questions() -> None:
    """
    Lädt Fragen aus questions.json in die Datenbank,
    falls die Tabelle noch leer ist.
    """
    seed_file = "questions.json"

    if not os.path.exists(seed_file):
        print(
            f"⚠️  Seed-Datei '{seed_file}' nicht gefunden – keine Fragen geladen.")
        return

    with get_session() as session:
        existing = session.query(Question).first()
        if existing is not None:
            return  # Datenbank bereits befüllt

        try:
            with open(seed_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for chapter, questions in data.items():
                for q in questions:
                    question = Question(
                        chapter=chapter,
                        question_text=q["question"],
                        correct_answer=q["answer"],
                    )
                    question.options = q["options"]
                    session.add(question)

            session.commit()
            print("✅ Fragen erfolgreich in die Datenbank geladen.")

        except (json.JSONDecodeError, KeyError, OSError) as e:
            session.rollback()
            print(f"❌ Fehler beim Laden der Seed-Daten: {e}")