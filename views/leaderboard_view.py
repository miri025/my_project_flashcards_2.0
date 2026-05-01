"""NiceGUI UI für das Leaderboard."""

from nicegui import ui
from services.result_service import ResultService


def show_leaderboard_view(on_back):
    """
    Zeigt das Leaderboard an.

    on_back: Callback-Funktion um zurück zum Quiz zu navigieren
    """
    result_service = ResultService()

    with ui.column().classes("w-full max-w-2xl mx-auto gap-4 p-4"):

        # Titel
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("🏆 Leaderboard").classes("text-3xl font-bold")
            ui.button("← Zurück", on_click=on_back).classes(
                "bg-gray-100 text-gray-700"
            )

        # Leaderboard laden
        leaderboard = result_service.get_leaderboard()

        if not leaderboard:
            with ui.card().classes("w-full p-6 text-center"):
                ui.label("Noch keine Einträge vorhanden.").classes(
                    "text-gray-500")
        else:
            # Tabellen-Header
            with ui.card().classes("w-full p-0 overflow-hidden"):
                with ui.row().classes(
                    "w-full bg-blue-600 text-white font-semibold px-4 py-2"
                ):
                    ui.label("Platz").classes("w-16")
                    ui.label("Name").classes("flex-1")
                    ui.label("Score").classes("w-20 text-center")
                    ui.label("Total").classes("w-20 text-center")
                    ui.label("%").classes("w-20 text-center")
                    ui.label("Datum").classes("w-36 text-right")

                # Einträge
                for rank, entry in enumerate(leaderboard, start=1):
                    # Abwechselnde Zeilenfarben
                    row_class = "bg-white" if rank % 2 == 0 else "bg-gray-50"

                    # Top 3 hervorheben
                    rank_label = str(rank)
                    if rank == 1:
                        rank_label = "🥇"
                    elif rank == 2:
                        rank_label = "🥈"
                    elif rank == 3:
                        rank_label = "🥉"

                    with ui.row().classes(
                        f"w-full {row_class} px-4 py-3 items-center"
                    ):
                        ui.label(rank_label).classes("w-16 font-semibold")
                        ui.label(entry["username"]).classes("flex-1")
                        ui.label(str(entry["best_score"])).classes(
                            "w-20 text-center font-semibold text-blue-600"
                        )
                        ui.label(str(entry["total"])).classes(
                            "w-20 text-center")
                        ui.label(f"{entry['percentage']}%").classes(
                            "w-20 text-center text-gray-600"
                        )
                        ui.label(entry["date"]).classes(
                            "w-36 text-right text-gray-400 text-sm"
                        )

        # Aktualisieren-Button
        ui.button(
            "🔄 Aktualisieren",
            on_click=lambda: ui.navigate.reload(),
        ).classes("w-full mt-2 bg-gray-100 text-gray-700")
