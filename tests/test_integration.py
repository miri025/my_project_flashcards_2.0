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
 