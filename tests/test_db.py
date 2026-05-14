from sqlmodel import select

from models.question import Question
from models.user import User
from models.result import Result


def test_questions_are_loaded_from_seeded_database(seeded_db):
    questions = seeded_db.exec(
        select(Question)
    ).all()

    assert len(questions) == 4
    assert questions[0].text is not None


def test_users_are_saved_in_database(seeded_db):
    users = seeded_db.exec(
        select(User)
    ).all()

    assert len(users) == 2
    assert users[0].username == "Max"


def test_saving_result_persists_leaderboard_entry(db):
    result = Result(
        username="albin",
        score=8
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    saved_result = db.exec(
        select(Result).where(
            Result.username == "albin"
        )
    ).first()

    assert saved_result is not None
    assert saved_result.score == 8