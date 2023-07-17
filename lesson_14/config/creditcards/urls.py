from django.urls import path
from . import views

urlpatterns = [
    path("card", views.create_card, name="create_card"),
    path("card/<uuid:card_id>", views.get_card, name="get_card"),
    path("card/<uuid:card_id>/activate", views.activate_card, name="activate_card"),
    path("card/<uuid:card_id>/block", views.block_card, name="block_card"),
    path("card/<uuid:card_id>/delete", views.delete_card, name="delete_card"),
]
