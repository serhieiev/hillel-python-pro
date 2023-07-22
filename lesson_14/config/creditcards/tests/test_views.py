from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.urls import reverse
from rest_framework import status
from ..models.card import Card, CardStatus
from uuid import UUID


class CardViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.card = Card.objects.create(
            card_number="4532015112830366",
            card_expire_date="2025-07-09",
            card_cvv="123",
            card_issue_date="2022-07-09",
            card_holder_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            card_status=CardStatus.NEW.value,
            owner=self.user,
        )

    def test_retrieve_card(self):
        url = reverse(
            "creditcards:cards-retrieve-update", kwargs={"pk": self.card.card_id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["card_id"], str(self.card.card_id))
        self.assertEqual(response.data["card_holder_id"], str(self.card.card_holder_id))
        self.assertEqual(response.data["card_status"], self.card.card_status)
        self.assertEqual(
            response.data["card_issue_date"], str(self.card.card_issue_date)
        )
        self.assertEqual(
            response.data["card_expire_date"], str(self.card.card_expire_date)
        )
        self.assertEqual(response.data["card_holder_id"], str(self.card.card_holder_id))

    def test_list_cards(self):
        url = reverse("creditcards:cards-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_card(self):
        url = reverse("creditcards:cards-list-create")
        data = {
            "card_number": "4532015112830366",
            "card_expire_date": "2025-07-09",
            "card_cvv": "123",
            "card_issue_date": "2022-07-09",
            "card_holder_id": "123e4567-e89b-12d3-a456-426614174000",
            "card_status": CardStatus.NEW.value,
            "owner": self.user.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activate_card(self):
        # Set the card status to NEW before attempting to activate
        self.card.card_status = CardStatus.NEW.value
        self.card.save()

        url = reverse("creditcards:activate-card", kwargs={"pk": self.card.card_id})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        self.assertEqual(self.card.card_status, CardStatus.ACTIVE.value)

    def test_freeze_card(self):
        # Set the card status to ACTIVE before attempting to freeze
        self.card.card_status = CardStatus.ACTIVE.value
        self.card.save()

        url = reverse("creditcards:freeze-card", kwargs={"pk": self.card.card_id})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        self.assertEqual(self.card.card_status, CardStatus.FROZEN.value)

    def test_reactivate_card(self):
        # Set the card status to FROZEN before attempting to reactivate
        self.card.card_status = CardStatus.FROZEN.value
        self.card.save()

        url = reverse("creditcards:reactivate-card", kwargs={"pk": self.card.card_id})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        self.assertEqual(self.card.card_status, CardStatus.ACTIVE.value)

    def test_set_card_name(self):
        url = reverse("creditcards:set-card-name", kwargs={"pk": self.card.card_id})
        data = {"card_name": "New Card Name"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        self.assertEqual(self.card.card_name, data["card_name"])
