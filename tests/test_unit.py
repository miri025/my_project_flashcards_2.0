import pytest

from services.quiz_service import QuizService
from services.result_service import ResultService
from services.user_service import UserService


def test_make_summary_calculates_percentage():
    service = ResultService()

    summary = service.make_summary(
        username="testuser",
        score=3,
        total=4,
        aborted=False,
    )

    assert summary["score"] == 3
    assert summary["total"] == 4
    assert summary["percentage"] == 75.0


def test_username_validation_rejects_empty_username():
    service = UserService()

    is_valid, message = service.validate_username("")

    assert is_valid is False
    assert message == "Benutzername darf nicht leer sein."


def test_question_count_accepts_choice_1_2_3():
    service = QuizService()

    assert service.validate_question_count("1", 30) == (True, 10)
    assert service.validate_question_count("2", 30) == (True, 20)
    assert service.validate_question_count("3", 30) == (True, 30)


def test_question_count_rejects_invalid_number():
    service = QuizService()

    is_valid, message = service.validate_question_count("4", 30)

    assert is_valid is False
    assert message == "Ungültige Eingabe. Bitte 1, 2 oder 3 eingeben."