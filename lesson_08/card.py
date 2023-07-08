import os
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from db_manager import DatabaseManager
from uuid import UUID, uuid4
from datetime import date
from enum import Enum
from typing import Optional


class CardStatus(Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"


class Card:
    def __init__(
        self,
        card_number: str,
        card_expire_date: str,
        card_cvv: str,
        card_issue_date: date,
        card_holder_id: UUID,
        card_status: CardStatus,
        card_id: UUID = None,
    ):
        self.card_id = card_id if card_id is not None else uuid4()
        self.card_number = card_number
        self.card_expire_date = card_expire_date
        self.card_cvv = card_cvv
        self.card_issue_date = card_issue_date
        self.card_holder_id = card_holder_id
        self.card_status = card_status

    def encrypt_data(self, data):
        # Generate cipher suite
        cipher_suite = Fernet(os.getenv("SECRET_KEY"))
        # Encrypt data
        encrypted_data = cipher_suite.encrypt(data.encode())
        # Convert bytes to string for storage
        return encrypted_data.decode()

    @staticmethod
    def decrypt_data(encrypted_data):
        # Convert from string to bytes
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        # Generate cipher suite
        cipher_suite = Fernet(os.getenv("SECRET_KEY"))
        # Decrypt data
        return cipher_suite.decrypt(encrypted_data).decode()

    def save(self):
        # connect to DB
        conn = DatabaseManager.get_connection()
        cur = DatabaseManager.get_cursor(conn)

        # Encrypt sensitive data
        encrypted_card_number = self.encrypt_data(self.card_number)
        encrypted_card_cvv = self.encrypt_data(self.card_cvv)

        # Check if the card already exists in the DB
        cur.execute(
            "SELECT card_id FROM cards WHERE card_id = %s", (str(self.card_id),)
        )
        result = cur.fetchone()

        if result:
            # If the card exists, update it
            cur.execute(
                """
                UPDATE Cards
                SET card_number = %s, card_expire_date = %s, card_cvv = %s, card_issue_date = %s, card_holder_id = %s, card_status = %s
                WHERE card_id = %s
                """,
                (
                    encrypted_card_number,
                    self.card_expire_date,
                    encrypted_card_cvv,
                    self.card_issue_date.strftime("%Y-%m-%d"),
                    str(self.card_holder_id),
                    self.card_status.value,
                    str(self.card_id),
                ),
            )
        else:
            # If the card doesn't exist, insert it
            cur.execute(
                """
                INSERT INTO cards (card_id, card_number, card_expire_date, card_cvv, card_issue_date, card_holder_id, card_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    str(self.card_id),
                    encrypted_card_number,
                    self.card_expire_date,
                    encrypted_card_cvv,
                    self.card_issue_date.strftime("%Y-%m-%d"),
                    str(self.card_holder_id),
                    self.card_status.value,
                ),
            )

        conn.commit()
        conn.close()

    @staticmethod
    def load_from_db(card_id: UUID) -> Optional["Card"]:
        # connect to DB
        conn = DatabaseManager.get_connection()
        cur = DatabaseManager.get_cursor(conn)

        # execute the query
        cur.execute(
            """
            SELECT card_id, card_number, card_expire_date, card_cvv, card_issue_date, card_holder_id, card_status 
            FROM cards
            WHERE card_id = %s
            """,
            (str(card_id),),
        )

        result = cur.fetchone()
        conn.close()

        if result is not None:
            (
                card_id,
                card_number,
                card_expire_date,
                card_cvv,
                card_issue_date,
                card_holder_id,
                card_status,
            ) = result

            # Decrypt sensitive data
            decrypted_card_number = Card.decrypt_data(card_number)
            decrypted_card_cvv = Card.decrypt_data(card_cvv)

            return Card(
                decrypted_card_number,
                card_expire_date,
                decrypted_card_cvv,
                card_issue_date,
                UUID(card_holder_id),
                CardStatus(card_status),
                UUID(card_id),
            )
        else:
            return None

    def activate(self):
        if self.card_status == CardStatus.BLOCKED:
            raise ValueError("Cannot activate a blocked card")
        self.card_status = CardStatus.ACTIVE
        self.save()

    def block(self):
        self.card_status = CardStatus.BLOCKED
        self.save()

    def __str__(self):
        return f"Card(card_number={self.mask_card_number()}, card_expire_date={self.card_expire_date}, card_cvv=***, card_issue_date={self.card_issue_date}, card_holder_id={self.card_holder_id}, card_status={self.card_status}, card_id={self.card_id})"

    def mask_card_number(self) -> str:
        """
        This function masks the card number to protect it from being displayed.
        Only the last 4 digits will be visible.
        """
        return "*" * (len(self.card_number) - 4) + self.card_number[-4:]
