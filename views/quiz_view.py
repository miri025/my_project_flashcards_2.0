"""NiceGUI UI für die Quiz-Durchführung."""

from nicegui import ui
from services.quiz_service import QuizService
from services.result_service import ResultService
from models.user import User

def show_quiz_view(user: User, on_quiz_done):
    """
    Zeigt die Quiz-Seite an.
 
    user: eingeloggter User
    on_quiz_done: Callback nach Abschluss des Quiz, erhält summary-Dict
    """
    quiz_service = QuizService()
    result_service = ResultService()
 
    # Quiz-Zustand
    state = {
        "questions": [],
        "current_index": 0,
        "score": 0,
        "aborted": False,
        "phase": "setup",  # setup | quiz | done
    }
 
    # Haupt-Container (wird bei Phasenwechsel geleert und neu befüllt)
    container = ui.column().classes("w-full max-w-2xl mx-auto gap-4 p-4")
 
    def show_setup():
        """Zeigt die Quiz-Einstellungen (Kapitel & Fragenanzahl)."""
        container.clear()
        state["phase"] = "setup"
 
        with container:
            ui.label(f"👋 Hallo, {user.username}!").classes(
                "text-2xl font-bold")
            ui.label("Quiz einrichten").classes("text-xl font-semibold")
 
            # Kapitel laden
            chapters = quiz_service.get_available_chapters()
            if not chapters:
                ui.label("❌ Keine Fragen in der Datenbank gefunden.").classes(
                    "text-red-500")
                return
 
            with ui.card().classes("w-full p-4"):
                ui.label("Kapitel auswählen").classes("font-semibold mb-2")
 
                chapter_options = {"Alle Kapitel": "all"}
                for i, chapter in enumerate(chapters, start=1):
                    chapter_options[f"{i}) {chapter}"] = str(i)
 
                chapter_select = ui.select(
                    options=list(chapter_options.keys()),
                    value="Alle Kapitel",
                    label="Kapitel",
                ).classes("w-full")
 
            with ui.card().classes("w-full p-4"):
                ui.label("Anzahl Fragen").classes("font-semibold mb-2")
 
                count_select = ui.select(
                    options=["10 Fragen", "20 Fragen", "30 Fragen"],
                    value="10 Fragen",
                    label="Anzahl",
                ).classes("w-full")
 
            error_label = ui.label("").classes("text-red-500 text-sm")
 
            def start_quiz():
                """Verarbeitet die Einstellungen und startet das Quiz."""
                error_label.set_text("")
 
                # Kapitelauswahl auflösen
                selected_label = chapter_select.value
                raw_selection = chapter_options[selected_label]
 
                valid, result = quiz_service.validate_chapter_selection(
                    raw_selection, chapters
                )
                if not valid:
                    error_label.set_text(f"⚠️ {result}")
                    return
 
                selected_chapters = result
 
                # Fragen laden und mischen
                questions = quiz_service.get_questions_by_chapters(
                    selected_chapters)
                questions = quiz_service.shuffle_questions(questions)
 
                # Fragenanzahl auflösen
                count_map = {"10 Fragen": "1",
                             "20 Fragen": "2", "30 Fragen": "3"}
                raw_count = count_map[count_select.value]
 
                valid_count, count_result = quiz_service.validate_question_count(
                    raw_count, len(questions)
                )
                if not valid_count:
                    error_label.set_text(f"⚠️ {count_result}")
                    return
 
                state["questions"] = quiz_service.select_questions(
                    questions, count_result
                )
                state["current_index"] = 0
                state["score"] = 0
                state["aborted"] = False
 
                show_question()
 
            ui.button("Quiz starten", on_click=start_quiz).classes(
                "w-full mt-2 bg-blue-600 text-white"
            )
 
    def show_question():
        """Zeigt die aktuelle Frage an."""
        container.clear()
        state["phase"] = "quiz"
 
        questions = state["questions"]
        index = state["current_index"]
 
        # Quiz beendet
        if index >= len(questions):
            show_done()
            return
 
        question = questions[index]
        question_number = index + 1
        total = len(questions)
 
        with container:
            # Fortschritt
            ui.label(f"Frage {question_number} von {total}").classes(
                "text-gray-500 text-sm"
            )
            ui.linear_progress(value=question_number / total).classes("w-full")
 
            with ui.card().classes("w-full p-6"):
                ui.label(f"📚 {question.chapter}").classes(
                    "text-sm text-gray-400 mb-2")
                ui.label(question.question_text).classes(
                    "text-lg font-semibold mb-4")
 
                feedback_label = ui.label("").classes(
                    "text-base font-semibold mt-2")
 
                def handle_answer(answer_num: int, btn):
                    """Verarbeitet die gewählte Antwort."""
                    is_correct = quiz_service.check_answer(
                        question, answer_num)
 
                    if is_correct:
                        state["score"] += 1
                        feedback_label.set_text("✅ Richtig!")
                        feedback_label.classes(
                            "text-green-600", remove="text-red-600")
                        btn.classes("bg-green-500", remove="bg-gray-100")
                    else:
                        feedback_label.set_text(
                            f"❌ Falsch. Richtig wäre: "
                            f"{question.options[question.correct_answer - 1]}"
                        )
                        feedback_label.classes(
                            "text-red-600", remove="text-green-600")
                        btn.classes("bg-red-400", remove="bg-gray-100")
 
                    # Alle Buttons deaktivieren
                    for b in answer_buttons:
                        b.props("disabled")
 
                    next_button.props(remove="disabled")
 
                answer_buttons = []
 
                for i, option in enumerate(question.options, start=1):
                    btn = ui.button(
                        option,
                        on_click=lambda num=i, b=None: None,
                    ).classes("w-full text-left bg-gray-100 text-black")
 
                    # Closure korrekt setzen
                    btn.on("click", lambda _, num=i,
                           b=btn: handle_answer(num, b))
 
                    answer_buttons.append(btn)
 
                def go_next():
                    state["current_index"] += 1
                    show_question()
 
                # JETZT unter den Antworten
                next_button = ui.button(
                    "Nächste Frage",
                    on_click=lambda: go_next()
                ).classes(
                    "w-full mt-4 bg-blue-600 text-white"
                ).props("disabled")
 
            # Abbrechen-Button
            def abort_quiz():
                state["aborted"] = True
                show_done()
 
            ui.button("Quiz abbrechen", on_click=abort_quiz).classes(
                "w-full mt-2 bg-red-100 text-red-600"
            )
 
    def show_done():
        """Zeigt die Auswertung und speichert das Ergebnis."""
        container.clear()
        state["phase"] = "done"
 
        score = state["score"]
        total = state["current_index"]
        aborted = state["aborted"]
 
        # Ergebnis in DB speichern
        result_service.save_result(
            user_id=user.id,
            score=score,
            total=total,
            aborted=aborted,
        )
 
        summary = result_service.make_summary(
            username=user.username,
            score=score,
            total=total,
            aborted=aborted,
        )
 
        with container:
            ui.label("🏁 Quiz abgeschlossen!").classes(
                "text-2xl font-bold text-center")
 
            with ui.card().classes("w-full p-6 text-center"):
                if aborted:
                    ui.label("⚠️ Quiz wurde vorzeitig abgebrochen.").classes(
                        "text-orange-500 mb-2"
                    )
 
                ui.label(f"Richtige Antworten: {score} / {total}").classes(
                    "text-xl font-semibold"
                )
                ui.label(f"Trefferquote: {summary['percentage']}%").classes(
                    "text-gray-600"
                )
                ui.label(f"Datum: {summary['date']}").classes(
                    "text-gray-400 text-sm mt-2")
 
            with ui.row().classes("w-full gap-2"):
                ui.button("Nochmal spielen", on_click=show_setup).classes(
                    "flex-1 bg-blue-600 text-white"
                )
                ui.button("Leaderboard", on_click=lambda: on_quiz_done(summary)).classes(
                    "flex-1 bg-green-600 text-white"
                )
 
    # Quiz starten mit Setup-Phase
    show_setup()