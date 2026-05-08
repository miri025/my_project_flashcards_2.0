"""Businesslogik für die Benutzerverwaltung."""

from sqlalchemy.exc import SQLAlchemyError
from models.database import get_session
from models.user import User


class UserService:
    """Verwaltet alle Operationen rund um Benutzer."""

    def validate_username(self, username: str) -> tuple[bool, str]:
        """
        Prüft ob der Benutzername die Regeln erfüllt.

        Regeln:
        - Nicht leer
        - Keine Leerzeichen
        - Mindestens 5 Zeichen
        - Mindestens ein Buchstabe und eine Ziffer

        Rückgabe: (True, "") wenn gültig, sonst (False, Fehlermeldung)
        """
        if not username:
            return False, "Benutzername darf nicht leer sein."

        if " " in username:
            return False, "Benutzername darf keine Leerzeichen enthalten."

        if len(username) < 5:
            return False, "Benutzername muss mindestens 5 Zeichen lang sein."

        has_letter = any(ch.isalpha() for ch in username)
        has_digit = any(ch.isdigit() for ch in username)

        if not has_letter or not has_digit:
            return False, "Benutzername muss mindestens einen Buchstaben und eine Ziffer enthalten."

        return True, ""
    
    def check_username_availability(
        self,
        username: str
    ) -> tuple[bool, bool, str]:
        """
        Prüft ob der Benutzername gültig und bereits vergeben ist.

        Rückgabe:
        (
            is_valid,
            is_taken,
            message
        )
        """
        is_valid, message = self.validate_username(username)

        if not is_valid:
            return False, False, message

        is_taken = self.is_username_taken(username)

        if is_taken:
            return (
                True,
                True,
                (
                    "Benutzername bereits vergeben. "
                    "Du kannst trotzdem fortfahren "
                    "oder einen neuen wählen."
                )
            )

        return True, False, ""
 
    def is_username_taken(self, username: str) -> bool:
        """
        Prüft ob der Benutzername bereits in der Datenbank existiert.

        Rückgabe: True wenn vergeben, False wenn verfügbar
        """
        try:
            with get_session() as session:
                user = session.query(User).filter_by(username=username).first()
                return user is not None
        except SQLAlchemyError as e:
            print(f"❌ Datenbankfehler bei Usernamen-Prüfung: {e}")
            return False

    def register_user(self, username: str) -> User | None:
        """
        Registriert einen neuen Benutzer in der Datenbank.

        Rückgabe: User-Objekt wenn erfolgreich, None bei Fehler
        """
        try:
            with get_session() as session:
                new_user = User(username=username)
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                return new_user
        except SQLAlchemyError as e:
            print(f"❌ Fehler beim Registrieren des Benutzers: {e}")
            return None

    def get_user_by_username(self, username: str) -> User | None:
        """
        Gibt einen Benutzer anhand des Benutzernamens zurück.

        Rückgabe: User-Objekt oder None wenn nicht gefunden
        """
        try:
            with get_session() as session:
                user = session.query(User).filter_by(username=username).first()
                return user
        except SQLAlchemyError as e:
            print(f"❌ Datenbankfehler beim Laden des Benutzers: {e}")
            return None