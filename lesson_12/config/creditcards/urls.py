from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_cards, name='display_cards'),
    path('create', views.create_card_form, name='create_card_form'),
    path("card", views.create_card, name="create_card"),
    path("card/<uuid:card_id>", views.get_card, name="get_card"),
    path("card/<uuid:card_id>/activate", views.activate_card, name="activate_card"),
    path("card/<uuid:card_id>/block", views.block_card, name="block_card"),
    path("card/<uuid:card_id>/delete", views.delete_card, name="delete_card"),
]
