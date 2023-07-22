from rest_framework import serializers
from ..models.card import Card


class CardSerializer(serializers.ModelSerializer):
    masked_card_number = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            "card_id",
            "card_number",
            "masked_card_number",
            "card_expire_date",
            "card_cvv",
            "card_issue_date",
            "card_holder_id",
            "card_status",
            "created_at",
            "modified_at",
            "owner",
            "card_name",
        ]
        extra_kwargs = {
            "owner": {"write_only": True},
            "card_number": {"write_only": True},
            "card_cvv": {"write_only": True},
        }

    def get_masked_card_number(self, obj):
        return obj.mask_card_number()


class CardStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["card_status"]


class CardNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["card_name"]
