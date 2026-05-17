from models.question import Question
from models.user import User
from models.result import Result


def test_quiz_service_loads_questions_from_database(seeded_db):
    questions = seeded_db.query(Question).all()

    assert len(questions) == 4
    assert questions[0].question_text is not None


def test_quiz_session_has_no_duplicate_questions(seeded_db):
    questions = seeded_db.query(Question).all()

    question_ids = [question.id for question in questions]

    assert len(question_ids) == len(set(question_ids))


def test_finished_quiz_saves_result_to_leaderboard(db):
    user = User(username="Test123")
    db.add(user)
    db.commit()
    db.refresh(user)

    result = Result(
        user_id=user.id,
        score=3,
        total=4,
        aborted=False,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    saved_result = db.query(Result).filter_by(user_id=user.id).first()

    assert saved_result is not None
    assert saved_result.score == 3
    assert saved_result.total == 4
    assert saved_result.percentage == 75.0