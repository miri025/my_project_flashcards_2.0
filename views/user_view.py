"""NiceGUI UI für Login und Registrierung."""

from nicegui import ui
from services.user_service import UserService


def show_user_view(on_login_success):
    """
    Zeigt die Login/Registrierungs-Seite an.

    on_login_success: Callback-Funktion die nach erfolgreichem Login aufgerufen wird.
                      Erhält das User-Objekt als Parameter.
    """
    user_service = UserService()

    with ui.column().classes("absolute-center items-center gap-6 w-full max-w-md"):

        # Titel
        ui.label("🃏 FlashcardsPP").classes("text-4xl font-bold text-center")
        ui.label("Lerne smarter mit digitalen Karteikarten").classes(
            "text-gray-500 text-center"
        )

        # Eingabekarte
        with ui.card().classes("w-full p-6 shadow-lg"):
            ui.label(
                "Anmelden / Registrieren").classes("text-xl font-semibold mb-4")

            username_input = ui.input(
                label="Benutzername",
                placeholder="z.B. Anna1",
            ).classes("w-full")

            error_label = ui.label("").classes("text-red-500 text-sm")

            def handle_login():
                """Verarbeitet die Login/Registrierungs-Eingabe."""
                username = username_input.value.strip()
                error_label.set_text("")

                # Validierung
                valid, message = user_service.validate_username(username)
                if not valid:
                    error_label.set_text(f"⚠️ {message}")
                    return

                # Prüfen ob User bereits existiert
                if user_service.is_username_taken(username):
                    user = user_service.get_user_by_username(username)
                    ui.notify(
                        f"👤 Willkommen zurück, {username}!", type="positive")
                else:
                    user = user_service.register_user(username)
                    if user is None:
                        error_label.set_text(
                            "❌ Fehler beim Registrieren. Bitte erneut versuchen.")
                        return
                    ui.notify(
                        f"✅ Neuer Benutzer registriert: {username}", type="positive")

                on_login_success(user)

            ui.button("Weiter", on_click=handle_login).classes(
                "w-full mt-2 bg-blue-600 text-white"
            )

            # Enter-Taste unterstützen
            username_input.on("keydown.enter", handle_login)
