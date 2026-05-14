import pytest
from sqlmodel import Session, SQLModel

from models.question import Question
from models.user import User
from models.result import Result
from models.database import Database


@pytest.fixture(scope="function")
def database():
    db = Database("sqlite:///:memory:")

    SQLModel.metadata.create_all(db.engine)

    yield db

    SQLModel.metadata.drop_all(db.engine)


@pytest.fixture(scope="function")
def db(database):
    with Session(database.engine) as session:
        yield session


@pytest.fixture
def seeded_db(db):
    q1 = Question(
        chapter=1,
        text="Was ist Python?"
    )

    q2 = Question(
        chapter=1,
        text="Was ist eine Klasse?"
    )

    q3 = Question(
        chapter=2,
        text="Was ist SQL?"
    )

    q4 = Question(
        chapter=2,
        text="Was ist ein Primary Key?"
    )

    db.add_all([q1, q2, q3, q4])
    db.commit()

    for question in [q1, q2, q3, q4]:
        db.refresh(question)

    user1 = User(
        username="Max"
    )

    user2 = User(
        username="Anna"
    )

    db.add_all([user1, user2])
    db.commit()

    result1 = Result(
        username="Max",
        score=8
    )

    result2 = Result(
        username="Anna",
        score=10
    )

    db.add_all([result1, result2])
    db.commit()

    return db


@pytest.fixture
def sample_answers():
    return [True, False, True, True]