from django.test import TestCase
from uuid import UUID
from ..models import Card, CardStatus


class CardModelTest(TestCase):
    def setUp(self):
        self.card = Card.objects.create(
            card_number="4532015112830366",
            card_expire_date="2025-07-09",
            card_cvv="123",
            card_issue_date="2022-07-09",
            card_holder_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            card_status=CardStatus.NEW.value,
        )

    def test_is_valid(self):
        self.assertEqual(self.card.is_valid(), True)

    def test_invalid_card_non_string(self):
        self.card.card_number = 1234567812345678
        with self.assertRaises(ValueError):
            self.card.is_valid()

    def test_invalid_card_is_empty_string(self):
        self.card.card_number = ""
        with self.assertRaises(ValueError):
            self.card.is_valid()

    def test_invalid_card_with_alpha_chars(self):
        self.card.card_number = "1234abcd5678efgh"
        with self.assertRaises(ValueError):
            self.card.is_valid()

    def test_invalid_card_too_short(self):
        self.card.card_number = "12345678"
        with self.assertRaises(ValueError):
            self.card.is_valid()

    def test_invalid_card_failed_luhn(self):
        self.card.card_number = "1234567812345678"
        self.assertEqual(self.card.is_valid(), False)

    def test_activate(self):
        self.card.activate()
        self.assertEqual(self.card.card_status, CardStatus.ACTIVE.value)

    def test_block(self):
        self.card.block()
        self.assertEqual(self.card.card_status, CardStatus.BLOCKED.value)

    def test_activate_blocked_card(self):
        self.card.block()
        with self.assertRaises(ValueError):
            self.card.activate()

    def test_load_from_db(self):
        card = Card.load_from_db(self.card.card_id)
        self.assertEqual(card.card_id, self.card.card_id)

    def test_load_from_db_not_exist(self):
        card = Card.load_from_db(UUID("123e4567-e89b-12d3-a456-426614174002"))
        self.assertEqual(card, None)

    def test_delete_card(self):
        card_id = self.card.card_id
        self.card.delete_card()
        card = Card.load_from_db(card_id)
        self.assertEqual(card, None)
