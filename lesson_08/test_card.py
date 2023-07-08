import pytest
from flask import url_for
from uuid import uuid4
from datetime import datetime
from cards_app import create_app
from card import Card, CardStatus
from db_manager import DatabaseManager
import random
import string


# Generate random card number
def random_string(length):
    digits = string.digits
    return "".join(random.choice(digits) for i in range(length))


# Setup a fixture for the PostgreSQL connection
@pytest.fixture(scope="module")
def conn():
    conn = DatabaseManager.get_connection()
    yield conn
    conn.close()


# Setup a fixture for a test client
@pytest.fixture
def client(app):
    with app.app_context():
        with app.test_client() as client:
            yield client


# Fixture for a Flask app
@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SERVER_NAME": "localhost",
            "APPLICATION_ROOT": "/",
            "PREFERRED_URL_SCHEME": "http",
        }
    )
    return app


# Fixture for a test card in the database
@pytest.fixture
def test_card():
    card = Card(
        card_number=random_string(16),  # generate a random card number
        card_expire_date="2026-01-01",
        card_cvv="123",
        card_issue_date=datetime.now(),
        card_holder_id=uuid4(),
        card_status=CardStatus.ACTIVE,
        card_id=uuid4(),
    )
    card.save()
    yield card


# Test card can be saved to DB and then loaded
def test_save_and_load_from_db(test_card):
    loaded_card = Card.load_from_db(test_card.card_id)
    assert loaded_card.card_id == test_card.card_id
    assert loaded_card.card_number == test_card.card_number
    assert (
        loaded_card.card_expire_date.strftime("%Y-%m-%d") == test_card.card_expire_date
    )
    assert loaded_card.card_cvv == test_card.card_cvv
    assert loaded_card.card_issue_date == test_card.card_issue_date.date()
    assert loaded_card.card_holder_id == test_card.card_holder_id
    assert loaded_card.card_status == test_card.card_status


# Test card can be activated
def test_activate(test_card):
    test_card.activate()
    loaded_card = Card.load_from_db(test_card.card_id)
    assert loaded_card.card_status.value == test_card.card_status.value


# Test card can be blocked
def test_block(test_card):
    test_card.block()
    loaded_card = Card.load_from_db(test_card.card_id)
    assert loaded_card.card_status.value == test_card.card_status.value


# Test card number can be masked
def test_mask_card_number(test_card):
    masked_number = test_card.mask_card_number()
    assert masked_number.startswith("*" * 12)
    assert len(masked_number) == len(test_card.card_number)


# Test create card endpoint
def test_create_card_endpoint(client):
    response = client.post(
        url_for("create_card"),
        json={
            "card_number": "4111111111111111",
            "card_expire_date": "2026-01-01",
            "card_cvv": "123",
            "card_issue_date": "2023-01-01",
            "card_holder_id": "87654321-1234-1234-1234-123456789012",
            "card_status": "NEW",
        },
    )
    assert response.status_code == 201


# Test get card endpoint
def test_get_card_endpoint(client, test_card):
    response = client.get(url_for("get_card", card_id=test_card.card_id))
    assert response.status_code == 200


# Test activate card endpoint
def test_activate_card_endpoint(client, test_card):
    response = client.put(url_for("activate_card", card_id=test_card.card_id))
    assert response.status_code == 200


# Test the get card endpoint
def test_block_card_endpoint(client, test_card):
    response = client.put(url_for("block_card", card_id=test_card.card_id))
    assert response.status_code == 200
