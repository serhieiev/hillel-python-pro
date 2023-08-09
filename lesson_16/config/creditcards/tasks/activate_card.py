from ..models.card import Card, CardStatus
from celery import shared_task


@shared_task
def activate_card(card_id):
    card = Card.objects.get(card_id=card_id)
    card.card_status = CardStatus.ACTIVE.value
    card.save()
