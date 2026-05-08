"""NiceGUI UI für Login und Registrierung."""

from nicegui import ui

from services.user_service import UserService


def show_user_view(on_login_success):
    """
    Zeigt die Login- und Registrierungs-Seite an.

    on_login_success wird nach erfolgreichem Login aufgerufen.
    """
    user_service = UserService()

    with ui.column().classes("absolute-center items-center gap-6 w-full max-w-md"):
        ui.label("🃏 FlashcardsPP").classes("text-4xl font-bold text-center")
        ui.label("Lerne smarter mit digitalen Karteikarten").classes(
            "text-gray-500 text-center"
        )

        with ui.card().classes("w-full p-6 shadow-lg"):
            ui.label("Anmelden / Registrieren").classes(
                "text-xl font-semibold mb-4"
            )

            username_input = ui.input(
                label="Benutzername",
                placeholder="z.B. Anna1",
            ).classes("w-full")

            error_label = ui.label("").classes("text-red-500 text-sm")

            def continue_with_existing_user(username: str):
                """Meldet einen bestehenden Benutzer an."""
                user = user_service.get_user_by_username(username)

                if user is None:
                    error_label.set_text("❌ Benutzer konnte nicht geladen werden.")
                    return

                ui.notify(
                    f"👤 Willkommen zurück, {username}!",
                    type="positive",
                )
                on_login_success(user)

            def register_new_user(username: str):
                """Registriert einen neuen Benutzer."""
                user = user_service.register_user(username)

                if user is None:
                    error_label.set_text(
                        "❌ Fehler beim Registrieren. Bitte erneut versuchen."
                    )
                    return

                ui.notify(
                    f"✅ Neuer Benutzer registriert: {username}",
                    type="positive",
                )
                on_login_success(user)

            def show_username_taken_dialog(username: str):
                """Zeigt Auswahl an, wenn der Benutzername vergeben ist."""
                with ui.dialog() as dialog:
                    with ui.card().classes("p-6 gap-4"):
                        ui.label("Benutzername bereits vergeben").classes(
                            "text-xl font-semibold"
                        )
                        ui.label(
                            "Dieser Benutzername existiert bereits. "
                            "Du kannst trotzdem fortfahren oder einen "
                            "neuen Benutzernamen eingeben."
                        ).classes("text-gray-600")

                        with ui.row().classes("w-full justify-end gap-2"):
                            ui.button(
                                "Neuen Namen wählen",
                                on_click=dialog.close,
                            ).classes("bg-gray-200 text-gray-800")

                            ui.button(
                                "Trotzdem fortfahren",
                                on_click=lambda: (
                                    dialog.close(),
                                    continue_with_existing_user(username),
                                ),
                            ).classes("bg-blue-600 text-white")

                dialog.open()

            def handle_login():
                """Verarbeitet die Login- und Registrierungs-Eingabe."""
                username = username_input.value.strip()
                error_label.set_text("")

                valid, message = user_service.validate_username(username)

                if not valid:
                    error_label.set_text(f"⚠️ {message}")
                    return

                if user_service.is_username_taken(username):
                    show_username_taken_dialog(username)
                    return

                register_new_user(username)

            ui.button("Weiter", on_click=handle_login).classes(
                "w-full mt-2 bg-blue-600 text-white"
            )

            username_input.on("keydown.enter", handle_login)