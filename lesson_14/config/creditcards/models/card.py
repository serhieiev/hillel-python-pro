import os
from uuid import UUID, uuid4
from datetime import date
from enum import Enum
from django.db import models
from django.conf import settings
from fernet_fields import EncryptedTextField


class CardStatus(Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    FROZEN = "FROZEN"


class Card(models.Model):
    card_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    card_number = EncryptedTextField()
    card_issue_date = models.CharField(max_length=10)
    card_expire_date = models.CharField(max_length=10)
    card_cvv = EncryptedTextField()
    card_holder_id = models.UUIDField()
    card_name = models.CharField(max_length=255, blank=True)
    card_status = models.CharField(max_length=10, default=CardStatus.NEW.value)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        if not self.card_number or not isinstance(self.card_number, str):
            raise ValueError("Card number must be a non-empty string")

        if not self.card_number.isdigit():
            raise ValueError("Card number must only contain digits")

        # Visa, Mastercard and Discover are 16 digits, American Express employs a 15-digit format
        if len(self.card_number) < 15:
            raise ValueError("Card number is too short")

        digits = [int(d) for d in self.card_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum([int(d) for d in str(d * 2)])
        return checksum % 10 == 0

    def save(self, *args, **kwargs):
        self.card_number = self.encrypt_data(self.card_number)
        self.card_cvv = self.encrypt_data(self.card_cvv)
        super(Card, self).save(*args, **kwargs)

    def encrypt_data(self, data):
        return data  # Data will be encrypted by EncryptedTextField

    @staticmethod
    def decrypt_data(encrypted_data):
        return encrypted_data  # Data will be decrypted by EncryptedTextField

    @staticmethod
    def load_from_db(card_id: UUID):
        try:
            card = Card.objects.get(pk=card_id)
            card.card_number = Card.decrypt_data(card.card_number)
            card.card_cvv = Card.decrypt_data(card.card_cvv)
            return card
        except Card.DoesNotExist:
            return None

    def activate(self):
        if self.card_status == CardStatus.BLOCKED.value:
            raise ValueError("Cannot activate a blocked card")
        self.card_status = CardStatus.ACTIVE.value
        self.save()

    def block(self):
        self.card_status = CardStatus.BLOCKED.value
        self.save()

    def delete_card(self):
        self.delete()

    def __str__(self):
        return f"Card(card_number={self.mask_card_number()}, card_expire_date={self.card_expire_date}, card_cvv=***, card_issue_date={self.card_issue_date}, card_holder_id={self.card_holder_id}, card_status={self.card_status}, card_id={self.card_id})"

    def mask_card_number(self):
        return "*" * (len(self.card_number) - 4) + self.card_number[-4:]
