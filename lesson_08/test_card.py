import pytest
import sqlite3
from card import Card, CardStatus
from datetime import date
from uuid import uuid4


# Define fixture that represents DB
@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")  # Connect to an in-memory database for testing
    c = conn.cursor()
    # Create the Cards table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS Cards (
            card_id TEXT PRIMARY KEY,
            card_number TEXT NOT NULL,
            card_expire_date TEXT NOT NULL,
            card_cvv TEXT NOT NULL,
            card_issue_date TEXT NOT NULL,
            card_holder_id TEXT NOT NULL,
            card_status INTEGER NOT NULL
        )
    """
    )
    yield conn  # Provide the database connection to the test
    conn.close()  # Close the connection after the test is done


# Define fixture that represents a Card object
@pytest.fixture
def card(db):
    card = Card(
        card_number="1234567812345678",
        card_expire_date="10/2025",
        card_cvv="123",
        card_issue_date=date.today(),
        card_holder_id=uuid4(),
        card_status=CardStatus.NEW,
    )
    yield card
    c = db.cursor()
    c.execute(
        "DELETE FROM Cards WHERE card_id = ?", (str(card.card_id),)
    )  # Delete the card after the test is done
    db.commit()


# Test card can be activated
def test_card_activation(card):
    card.activate()

    assert card.card_status == CardStatus.ACTIVE


# Test card can be blocked
def test_card_blocking(card):
    card.block()

    assert card.card_status == CardStatus.BLOCKED


# Test card can be saved to DB and then loaded
def test_card_save_and_load_from_db(card, db):
    card.save_to_db()
    loaded_card = Card.load_from_db(card.card_id)

    assert loaded_card is not None
    assert loaded_card.card_id == card.card_id
    assert loaded_card.card_expire_date == card.card_expire_date
    assert loaded_card.card_issue_date == card.card_issue_date
    assert loaded_card.card_holder_id == card.card_holder_id
    assert loaded_card.card_status == card.card_status


# Test card number can be masked
def test_card_masking(card):
    masked_card_number = card.mask_card_number()

    assert masked_card_number == "************5678"
