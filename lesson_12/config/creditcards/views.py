from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Card, CardStatus
from uuid import UUID
from datetime import date
import json


def create_card_form(request):
    if request.method == "POST":
        data = request.POST

        card = Card(
            card_number=data["card_number"],
            card_expire_date=data["card_expire_date"],
            card_cvv=data["card_cvv"],
            card_issue_date=date.fromisoformat(data["card_issue_date"]),
            card_holder_id=UUID(data["card_holder_id"]),
            card_status=CardStatus(data["card_status"]).value,
        )

        if not card.is_valid():
            return render(request, 'creditcards/create_card_form.html', {"error": "Invalid card number"})

        card.save()

        return redirect('display_cards')
    return render(request, 'creditcards/create_card_form.html')


def display_cards(request):
    cards = Card.objects.all()
    return render(request, 'creditcards/display_cards.html', {'cards': cards})



@csrf_exempt
def create_card(request):
    if request.method == "POST":
        data = json.loads(request.body)

        card = Card(
            card_number=data["card_number"],
            card_expire_date=data["card_expire_date"],
            card_cvv=data["card_cvv"],
            card_issue_date=date.fromisoformat(data["card_issue_date"]),
            card_holder_id=UUID(data["card_holder_id"]),
            card_status=CardStatus(data["card_status"]).value,
        )

        if not card.is_valid():
            return JsonResponse({"error": "Invalid card number"}, status=400)

        card.save()

        return JsonResponse(
            {"message": "Card created", "card_id": str(card.card_id)}, status=201
        )


def get_card(request, card_id):
    try:
        card = Card.objects.get(card_id=card_id)
    except Card.DoesNotExist:
        raise Http404("Card does not exist")

    data = {
        "card_id": str(card.card_id),
        "card_number": card.card_number,  # Update this to mask card number
        "card_expire_date": card.card_expire_date,
        "card_cvv": "***",
        "card_issue_date": card.card_issue_date,
        "card_holder_id": str(card.card_holder_id),
        "card_status": card.card_status,
        "created_at": card.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        "modified_at": card.modified_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    return JsonResponse(data)


@csrf_exempt
def activate_card(request, card_id):
    if request.method == "PUT":
        try:
            card = Card.objects.get(card_id=card_id)
        except Card.DoesNotExist:
            return JsonResponse({"error": "Card not found"}, status=404)
        try:
            card.activate()
            card.save()  # Update this to save changes
            return JsonResponse({"status": "Card activated"})
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def block_card(request, card_id):
    if request.method == "PUT":
        try:
            card = Card.objects.get(card_id=card_id)
        except Card.DoesNotExist:
            return JsonResponse({"error": "Card not found"}, status=404)
        card.block()
        card.save()
        return JsonResponse({"status": "Card blocked"})


@csrf_exempt
def delete_card(request, card_id):
    if request.method == "DELETE":
        try:
            card = Card.objects.get(card_id=card_id)
        except Card.DoesNotExist:
            return JsonResponse({"error": "Card not found"}, status=404)
        card.delete()
        return JsonResponse({"status": "Card deleted"})
