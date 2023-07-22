from django.urls import path
from .views.cards_view import (
    CardListCreateAPIView,
    CardRetrieveUpdateAPIView,
    ActivateCardView,
    FreezeCardView,
    ReactivateCardView,
    SetCardNameView,
)

app_name = "creditcards"

urlpatterns = [
    path("cards/", CardListCreateAPIView.as_view(), name="cards-list-create"),
    path(
        "cards/<pk>/", CardRetrieveUpdateAPIView.as_view(), name="cards-retrieve-update"
    ),
    path("cards/<uuid:pk>/activate", ActivateCardView.as_view(), name="activate-card"),
    path("cards/<uuid:pk>/freeze", FreezeCardView.as_view(), name="freeze-card"),
    path(
        "cards/<uuid:pk>/reactivate",
        ReactivateCardView.as_view(),
        name="reactivate-card",
    ),
    path("cards/<uuid:pk>/setname", SetCardNameView.as_view(), name="set-card-name"),
]
