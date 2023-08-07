from celery import shared_task
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.card import Card, CardStatus
from ..serializers.card_serializers import (
    CardSerializer,
    CardStatusSerializer,
    CardNameSerializer,
)
from ..tasks.activate_card import activate_card
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCardOwner
from rest_framework.exceptions import NotFound


class CardListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cards = Card.objects.filter(owner=request.user)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            owner = validated_data.pop("owner", None)
            card = Card(**validated_data, owner=request.user)
            try:
                if card.is_valid():
                    card.save()
                    serializer = CardSerializer(card)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {"detail": "Invalid card"}, status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardRetrieveUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCardOwner]

    def get_object(self, pk):
        try:
            card = Card.objects.get(pk=pk)
            return card
        except Card.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        card = self.get_object(pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)


class BaseCardStatusView(generics.UpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardStatusSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsCardOwner]
    required_status = None
    new_status = None

    def patch(self, request, *args, **kwargs):
        card = self.get_object()
        if card.card_status != self.required_status.value:
            return Response(
                {"status": f"Card is not in {self.required_status} status"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        card.card_status = self.new_status.value
        card.save()
        return Response(self.get_serializer(card).data)


class ActivateCardView(BaseCardStatusView):
    required_status = CardStatus.NEW
    new_status = CardStatus.ACTIVE

    def patch(self, request, *args, **kwargs):
        card = self.get_object()
        if card.card_status != self.required_status.value:
            return super().patch(request, *args, **kwargs)

        activate_card.apply_async((card.card_id,), countdown=120)
        return Response(
            {"status": "activation scheduled"}, status=status.HTTP_202_ACCEPTED
        )


class FreezeCardView(BaseCardStatusView):
    required_status = CardStatus.ACTIVE
    new_status = CardStatus.FROZEN


class ReactivateCardView(BaseCardStatusView):
    required_status = CardStatus.FROZEN
    new_status = CardStatus.ACTIVE


class SetCardNameView(generics.UpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardNameSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsCardOwner]

    def patch(self, request, *args, **kwargs):
        card = self.get_object()
        serializer = self.get_serializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
