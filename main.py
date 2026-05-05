"""Einstiegspunkt der FlashcardsPP Web-Applikation."""

from nicegui import ui
from models.database import init_db
from views.user_view import show_user_view
from views.quiz_view import show_quiz_view
from views.leaderboard_view import show_leaderboard_view


def main():
    """
    Startet die FlashcardsPP Web-Applikation.

    Initialisiert die Datenbank und registriert die NiceGUI-Seiten.
    """
    # Datenbank initialisieren und Seed-Daten laden
    init_db()

    @ui.page("/")
    def index():
        """Startseite – Login/Registrierung."""
        ui.query("body").style("background-color: #f3f4f6")

        def on_login_success(user):
            """Nach erfolgreichem Login zur Quiz-Seite navigieren."""
            ui.navigate.to(f"/quiz/{user.id}/{user.username}")

        show_user_view(on_login_success=on_login_success)

    @ui.page("/quiz/{user_id}/{username}")
    def quiz(user_id: int, username: str):
        """Quiz-Seite."""
        ui.query("body").style("background-color: #f3f4f6")

        from services.user_service import UserService
        user_service = UserService()

        user = user_service.get_user_by_username(username)

        if user is None or user.id != user_id:
            ui.notify("❌ Benutzer nicht gefunden.", type="negative")
            ui.navigate.to("/")
            return

        def on_quiz_done(summary):
            """Nach dem Quiz zum Leaderboard navigieren."""
            ui.navigate.to("/leaderboard")

        show_quiz_view(user=user, on_quiz_done=on_quiz_done)

    @ui.page("/leaderboard")
    def leaderboard():
        """Leaderboard-Seite."""
        ui.query("body").style("background-color: #f3f4f6")

        def on_back():
            """Zurück zur Startseite navigieren."""
            ui.navigate.to("/")

        show_leaderboard_view(on_back=on_back)

    ui.run(
        title="FlashcardsPP",
        favicon="🃏",
        port=8080,
        reload=False,
    )


if __name__ == "__main__":
    main()