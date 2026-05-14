from sqlmodel import select
 
from models.question import Question
from models.result import Result
from services.quiz_service import QuizService
from services.result_service import ResultService
from services.user_service import UserService
 
 
def test_quiz_service_loads_questions_from_database(seeded_db):
    questions = seeded_db.exec(
        select(Question)
    ).all()
 
    assert len(questions) == 4
    assert questions[0].text is not None
 
 
def test_quiz_session_has_no_duplicate_questions(seeded_db):
    questions = seeded_db.exec(
        select(Question)
    ).all()
 
    question_ids = [question.id for question in questions]
 
    assert len(question_ids) == len(set(question_ids))
 
 
def test_finished_quiz_saves_result_to_leaderboard(db):
    result = Result(
        username="testuser",
        score=3
    )
 
    db.add(result)
    db.commit()
    db.refresh(result)
 
    saved_result = db.exec(
        select(Result).where(
            Result.username == "testuser"
        )
    ).first()
 
    assert saved_result is not None
    assert saved_result.username == "testuser"
    assert saved_result.score == 3