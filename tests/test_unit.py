import pytest
 
from services.quiz_service import QuizService
from services.result_service import ResultService
from services.user_service import UserService
 
 
def test_score_calculation_counts_correct_answers(sample_answers):
    service = ResultService()
 
    score = service.calculate_score(sample_answers)
 
    assert score == 3
 
 
def test_username_validation_rejects_empty_username():
    service = UserService()
 
    with pytest.raises(ValueError):
        service.validate_username("")
 
 
def test_question_count_accepts_only_10_20_30():
    service = QuizService()
 
    assert service.validate_question_count(10) == 10
    assert service.validate_question_count(20) == 20
    assert service.validate_question_count(30) == 30
 
 
def test_question_count_rejects_invalid_number():
    service = QuizService()
 
    with pytest.raises(ValueError):
        service.validate_question_count(15)