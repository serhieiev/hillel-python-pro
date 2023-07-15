from django.test import TestCase, Client
from django.template.loader import render_to_string
from ..models import Card, CardStatus
import json
from uuid import uuid4


class CardTestBase(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_card_data = {
            "card_number": "5265532938790574",
            "card_expire_date": "2027-07-10",
            "card_cvv": "123",
            "card_issue_date": "2023-07-10",
            "card_holder_id": str(uuid4()),
            "card_status": CardStatus.NEW.value,
        }

        self.card = Card.objects.create(**self.valid_card_data)
        self.card_id = str(self.card.card_id)


class CreateCardFormViewTest(CardTestBase):
    def test_display_create_card_form(self):
        response = self.client.get("/create")
        self.assertEqual(response.status_code, 200)
        
        html_content = str(response.content, encoding='utf8')

        # Check the form
        self.assertIn('<form action="/create" method="POST">', html_content)

        # Check the input fields
        self.assertIn('<input type="text" id="card_number" name="card_number" required', html_content)
        self.assertIn('<input type="date" id="card_expire_date" name="card_expire_date" required', html_content)
        self.assertIn('<input type="password" id="card_cvv" name="card_cvv" required', html_content)
        self.assertIn('<input type="date" id="card_issue_date" name="card_issue_date" required', html_content)
        self.assertIn('<input type="text" id="card_holder_id" name="card_holder_id" required', html_content)

        # Check the select field
        self.assertIn('<select id="card_status" name="card_status" required', html_content)

        # Check the options in the select field
        self.assertIn('<option value="">Select...</option>', html_content)
        self.assertIn('<option value="NEW">NEW</option>', html_content)
        self.assertIn('<option value="ACTIVE">ACTIVE</option>', html_content)
        self.assertIn('<option value="BLOCKED">BLOCKED</option>', html_content)

        # Check the submit button
        self.assertIn('<input type="submit" value="Create Card"', html_content)

    def test_create_card_form_post_with_valid_data(self):
        response = self.client.post("/create", self.valid_card_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_create_card_form_post_with_invalid_data(self):
        invalid_card_data = self.valid_card_data.copy()
        invalid_card_data["card_number"] = "1234567812345678"
        response = self.client.post("/create", invalid_card_data)
        self.assertContains(response, "Invalid card number", status_code=200)


class DisplayCardsViewTest(CardTestBase):
    def test_display_cards_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        expected_html = render_to_string(
            "creditcards/display_cards.html", {"cards": [self.card]}
        )
        self.assertHTMLEqual(str(response.content, encoding="utf8"), expected_html)


class CardViewTest(CardTestBase):
    def test_create_card(self):
        response = self.client.post(
            "/card",
            data=json.dumps(self.valid_card_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "Card created")
        self.assertIn("card_id", response_data)

    def test_create_card_invalid_card_number(self):
        invalid_card_data = self.valid_card_data.copy()
        invalid_card_data["card_number"] = "3706861257307453"
        response = self.client.post(
            "/card", data=json.dumps(invalid_card_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Invalid card number")

    def test_get_card(self):
        response = self.client.get(f"/card/{self.card_id}")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["card_id"], self.card_id)

    def test_get_card_not_found(self):
        response = self.client.get("/card/non_existent_card_id")
        self.assertEqual(response.status_code, 404)

    def test_activate_card(self):
        response = self.client.put(f"/card/{self.card_id}/activate")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["status"], "Card activated")

    def test_block_card(self):
        response = self.client.put(f"/card/{self.card_id}/block")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["status"], "Card blocked")

    def test_activate_blocked_card(self):
        # Block the card
        response = self.client.put(f"/card/{self.card_id}/block")
        self.assertEqual(response.status_code, 200)

        # Try to activate the blocked card
        response = self.client.put(f"/card/{self.card_id}/activate")
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["error"], "Cannot activate a blocked card")

    def test_delete_card(self):
        response = self.client.delete(f"/card/{self.card_id}/delete")
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["status"], "Card deleted")

        # Check that card is actually deleted
        response = self.client.get(f"/card/{self.card_id}/")
        self.assertEqual(response.status_code, 404)
