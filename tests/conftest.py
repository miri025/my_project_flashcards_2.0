import os
import sys
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.base import Base
from models.question import Question
from models.user import User
from models.result import Result


@pytest.fixture(scope="function")
def engine():
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db(engine):
    TestingSessionLocal = sessionmaker(bind=engine)

    with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def seeded_db(db):
    q1 = Question(
        chapter="Python",
        question_text="Was ist Python?",
        correct_answer=1,
    )
    q1.options = [
        "Eine Programmiersprache",
        "Eine Datenbank",
        "Ein Betriebssystem",
        "Ein Browser",
    ]

    q2 = Question(
        chapter="Python",
        question_text="Was ist eine Klasse?",
        correct_answer=1,
    )
    q2.options = [
        "Ein Bauplan für Objekte",
        "Eine Schleife",
        "Eine Variable",
        "Eine Datei",
    ]

    q3 = Question(
        chapter="Datenbanken",
        question_text="Was ist SQL?",
        correct_answer=1,
    )
    q3.options = [
        "Eine Datenbanksprache",
        "Ein Quiz",
        "Ein Webserver",
        "Ein Diagramm",
    ]

    q4 = Question(
        chapter="Datenbanken",
        question_text="Was ist ein Primary Key?",
        correct_answer=1,
    )
    q4.options = [
        "Ein eindeutiger Schlüssel",
        "Eine Antwortoption",
        "Ein Kapitel",
        "Ein Username",
    ]

    user1 = User(username="Max123")
    user2 = User(username="Anna123")

    db.add_all([q1, q2, q3, q4, user1, user2])
    db.commit()

    for item in [q1, q2, q3, q4, user1, user2]:
        db.refresh(item)

    result1 = Result(
        user_id=user1.id,
        score=8,
        total=10,
        aborted=False,
    )

    result2 = Result(
        user_id=user2.id,
        score=10,
        total=10,
        aborted=False,
    )

    db.add_all([result1, result2])
    db.commit()

    return db


@pytest.fixture
def sample_answers():
    return [True, False, True, True]