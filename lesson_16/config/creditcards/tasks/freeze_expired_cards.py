from datetime import datetime
from celery import shared_task


@shared_task
def freeze_expired_cards():
    from creditcards.models.card import Card, CardStatus

    current_date = datetime.today().date()

    cards = Card.objects.filter(card_expire_date__lt=current_date)
    for card in cards:
        card.card_status = CardStatus.FROZEN.value
        card.save()
