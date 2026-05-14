from models.question import Question
from models.user import User
from models.result import Result


def test_questions_are_loaded_from_seeded_database(seeded_db):
    questions = seeded_db.query(Question).all()

    assert len(questions) == 4
    assert questions[0].question_text is not None


def test_users_are_saved_in_database(seeded_db):
    users = seeded_db.query(User).all()

    assert len(users) == 2
    assert users[0].username == "Max123"


def test_saving_result_persists_leaderboard_entry(db):
    user = User(username="Test123")
    db.add(user)
    db.commit()
    db.refresh(user)

    result = Result(
        user_id=user.id,
        score=8,
        total=10,
        aborted=False,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    saved_result = db.query(Result).filter_by(user_id=user.id).first()

    assert saved_result is not None
    assert saved_result.score == 8
    assert saved_result.total == 10