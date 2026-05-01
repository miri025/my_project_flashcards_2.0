"""Businesslogik für Ergebnisse und Leaderboard."""

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from models.database import get_session
from models.result import Result
from models.user import User


class ResultService:
    """Verwaltet Quiz-Ergebnisse und das Leaderboard."""

    def save_result(
        self,
        user_id: int,
        score: int,
        total: int,
        aborted: bool,
    ) -> Result | None:
        """
        Speichert das Ergebnis einer Quiz-Session in der Datenbank.

        user_id: ID des Benutzers
        score: Anzahl richtig beantworteter Fragen
        total: Anzahl gestellter Fragen
        aborted: True wenn Quiz vorzeitig abgebrochen wurde

        Rückgabe: Result-Objekt oder None bei Fehler
        """
        try:
            with get_session() as session:
                result = Result(
                    user_id=user_id,
                    score=score,
                    total=total,
                    aborted=aborted,
                    played_at=datetime.now(),
                )
                session.add(result)
                session.commit()
                session.refresh(result)
                return result
        except SQLAlchemyError as e:
            print(f"❌ Fehler beim Speichern des Ergebnisses: {e}")
            return None

    def get_leaderboard(self) -> list[dict]:
        """
        Gibt das Leaderboard zurück.

        Jeder Eintrag enthält den besten Score des Benutzers.
        Sortiert nach Score absteigend.

        Rückgabe: Liste von Dictionaries mit username, best_score, total, date
        """
        try:
            with get_session() as session:
                users = session.query(User).all()
                leaderboard = []

                for user in users:
                    results = (
                        session.query(Result)
                        .filter_by(user_id=user.id)
                        .order_by(Result.score.desc())
                        .all()
                    )

                    if not results:
                        continue

                    best = results[0]
                    leaderboard.append({
                        "username": user.username,
                        "best_score": best.score,
                        "total": best.total,
                        "percentage": best.percentage,
                        "date": best.played_at.strftime("%Y-%m-%d %H:%M"),
                    })

                leaderboard.sort(key=lambda x: x["best_score"], reverse=True)
                return leaderboard

        except SQLAlchemyError as e:
            print(f"❌ Fehler beim Laden des Leaderboards: {e}")
            return []

    def get_results_by_user(self, user_id: int) -> list[Result]:
        """
        Gibt alle Ergebnisse eines Benutzers zurück, neueste zuerst.

        Rückgabe: Liste von Result-Objekten
        """
        try:
            with get_session() as session:
                results = (
                    session.query(Result)
                    .filter_by(user_id=user_id)
                    .order_by(Result.played_at.desc())
                    .all()
                )
                session.expunge_all()
                return results
        except SQLAlchemyError as e:
            print(f"❌ Fehler beim Laden der Benutzer-Ergebnisse: {e}")
            return []

    def make_summary(
        self,
        username: str,
        score: int,
        total: int,
        aborted: bool,
    ) -> dict:
        """
        Erstellt eine Zusammenfassung der abgeschlossenen Quiz-Session.

        Rückgabe: Dictionary mit allen relevanten Session-Daten
        """
        percentage = round(score / total * 100, 1) if total > 0 else 0.0

        return {
            "username": username,
            "score": score,
            "total": total,
            "percentage": percentage,
            "aborted": aborted,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
