"""Businesslogik für Quiz-Vorbereitung und Durchführung."""

import random
from sqlalchemy.exc import SQLAlchemyError
from models.database import get_session
from models.question import Question


class QuizService:
    """Verwaltet die gesamte Quiz-Logik."""

    def get_available_chapters(self) -> list[str]:
        """
        Gibt alle verfügbaren Kapitel aus der Datenbank zurück, sortiert.

        Rückgabe: Liste der Kapitelnamen
        """
        try:
            with get_session() as session:
                chapters = (
                    session.query(Question.chapter)
                    .distinct()
                    .order_by(Question.chapter)
                    .all()
                )
                return [row.chapter for row in chapters]
        except SQLAlchemyError as e:
            print(f"❌ Fehler beim Laden der Kapitel: {e}")
            return []

    def get_questions_by_chapters(self, chapters: list[str]) -> list[Question]:
        """
        Gibt alle Fragen der ausgewählten Kapitel zurück.

        chapters: Liste der ausgewählten Kapitelnamen
        Rückgabe: Liste von Question-Objekten
        """
        try:
            with get_session() as session:
                questions = (
                    session.query(Question)
                    .filter(Question.chapter.in_(chapters))
                    .all()
                )
                # Objekte aus Session lösen damit sie ausserhalb nutzbar sind
                session.expunge_all()
                return questions
        except SQLAlchemyError as e:
            print(f"❌ Fehler beim Laden der Fragen: {e}")
            return []

    def shuffle_questions(self, questions: list[Question]) -> list[Question]:
        """
        Mischt die Fragen zufällig.

        Rückgabe: zufällig sortierte Liste
        """
        shuffled = questions.copy()
        random.shuffle(shuffled)
        return shuffled

    def select_questions(
        self, questions: list[Question], count: int
    ) -> list[Question]:
        """
        Wählt eine bestimmte Anzahl Fragen aus der gemischten Liste aus.

        count: gewünschte Anzahl Fragen
        Rückgabe: gekürzte Liste (maximal count Einträge)
        """
        return questions[:count]

    def validate_chapter_selection(
        self, selection: str, available_chapters: list[str]
    ) -> tuple[bool, list[str] | str]:
        """
        Validiert die Kapitelauswahl des Benutzers.

        selection: Eingabe des Benutzers ("all" oder eine Zahl)
        available_chapters: Liste aller verfügbaren Kapitel

        Rückgabe: (True, ausgewählte Kapitel) oder (False, Fehlermeldung)
        """
        if selection.strip().lower() == "all":
            return True, available_chapters

        if selection.strip().isdigit():
            index = int(selection.strip())
            if 1 <= index <= len(available_chapters):
                return True, [available_chapters[index - 1]]

        return False, (
            f"Ungültige Eingabe. Bitte eine Zahl zwischen 1 und "
            f"{len(available_chapters)} eingeben oder 'all'."
        )

    def validate_question_count(
        self, selection: str, max_questions: int
    ) -> tuple[bool, int | str]:
        """
        Validiert die gewünschte Fragenanzahl.

        selection: Eingabe des Benutzers ("1", "2" oder "3")
        max_questions: maximal verfügbare Fragen

        Rückgabe: (True, Anzahl) oder (False, Fehlermeldung)
        """
        valid_choices = {"1": 10, "2": 20, "3": 30}

        if selection.strip() not in valid_choices:
            return False, "Ungültige Eingabe. Bitte 1, 2 oder 3 eingeben."

        chosen = valid_choices[selection.strip()]

        if chosen > max_questions:
            return True, max_questions

        return True, chosen

    def check_answer(self, question: Question, answer_number: int) -> bool:
        """
        Prüft ob die gegebene Antwort korrekt ist.

        question: Question-Objekt
        answer_number: vom Benutzer gewählte Nummer (1-4)

        Rückgabe: True wenn korrekt, sonst False
        """
        return answer_number == question.correct_answer
    