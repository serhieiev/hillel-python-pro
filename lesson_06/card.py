import os
from datetime import date
from uuid import UUID, uuid4
from enum import Enum
from typing import Optional
import sqlite3
from cryptography.fernet import Fernet


key = os.getenv("SECRET_KEY")
cipher_suite = Fernet(key)


class CardStatus(Enum):
    NEW = 1
    ACTIVE = 2
    BLOCKED = 3


class Card:
    def __init__(
        self,
        card_number: str,
        card_expire_date: str,
        card_cvv: str,
        card_issue_date: date,
        card_holder_id: uuid4,
        card_status: CardStatus,
        card_id: uuid4 = None,
    ):
        self.card_id = card_id if card_id is not None else uuid4()
        self.card_number = cipher_suite.encrypt(
            card_number.encode()
        ).decode()  # Encrypt the card number
        self.card_expire_date = card_expire_date
        self.card_cvv = cipher_suite.encrypt(
            card_cvv.encode()
        ).decode()  # Encrypt the CVV
        self.card_issue_date = card_issue_date
        self.card_holder_id = card_holder_id
        self.card_status = card_status

    def save_to_db(self):
        # connect to DB
        conn = sqlite3.connect("cards.db")
        c = conn.cursor()

        # Check if the card already exists in the DB
        c.execute("SELECT card_id FROM Cards WHERE card_id = ?", (str(self.card_id),))
        result = c.fetchone()

        if result:
            # If the card exists, update it
            c.execute(
                """
            UPDATE Cards
            SET card_number = ?, card_expire_date = ?, card_cvv = ?, card_issue_date = ?, card_holder_id = ?, card_status = ?
            WHERE card_id = ?
            """,
                (
                    self.card_number,
                    self.card_expire_date,
                    self.card_cvv,
                    self.card_issue_date.strftime("%Y-%m-%d"),
                    str(self.card_holder_id),
                    self.card_status.value,
                    str(self.card_id),
                ),
            )
        else:
            # If the card doesn't exist, insert it
            c.execute(
                """
            INSERT INTO Cards (card_id, card_number, card_expire_date, card_cvv, card_issue_date, card_holder_id, card_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    str(self.card_id),
                    self.card_number,
                    self.card_expire_date,
                    self.card_cvv,
                    self.card_issue_date.strftime("%Y-%m-%d"),
                    str(self.card_holder_id),
                    self.card_status.value,
                ),
            )

        conn.commit()

    @staticmethod
    def load_from_db(card_id: uuid4) -> Optional["Card"]:
        # connect to DB
        conn = sqlite3.connect("cards.db")
        c = conn.cursor()

        # execute the query
        c.execute(
            """
      SELECT card_id, card_number, card_expire_date, card_cvv, card_issue_date, card_holder_id, card_status
      FROM Cards
      WHERE card_id = ?
      """,
            (str(card_id),),
        )

        result = c.fetchone()
        conn.close()

        if result is None:
            return None

        (
            card_id,
            card_number,
            card_expire_date,
            card_cvv,
            card_issue_date,
            card_holder_id,
            card_status,
        ) = result

        card = Card(
            # card_number,
            cipher_suite.decrypt(
                card_number.encode()
            ).decode(),  # Decrypt the card number
            card_expire_date,
            cipher_suite.decrypt(card_cvv.encode()).decode(),  # Decrypt the CVV
            date.fromisoformat(card_issue_date),
            UUID(card_holder_id),
            CardStatus(card_status),
            UUID(card_id),
        )

        return card

    def activate(self):
        if self.card_status == CardStatus.BLOCKED:
            raise ValueError("Cannot activate a blocked card")
        self.card_status = CardStatus.ACTIVE
        self.save_to_db()

    def block(self):
        self.card_status = CardStatus.BLOCKED
        self.save_to_db()

    def mask_card_number(self) -> str:
        """
        This function masks the card number to protect it from being displayed.
        Only last 4 digits will be visible.
        """
        decrypted_card_number = cipher_suite.decrypt(
            self.card_number.encode()
        ).decode()  # Decrypt the card number
        return "*" * (len(decrypted_card_number) - 4) + decrypted_card_number[-4:]
