from flask import Flask, request, jsonify, make_response
from card import Card, CardStatus
from uuid import UUID, uuid4
from datetime import date


def create_app():
    app = Flask(__name__)

    # Endpoint to create a new card
    @app.route("/card", methods=["POST"])
    def create_card():
        data = request.json

        card = Card(
            data["card_number"],
            data["card_expire_date"],
            data["card_cvv"],
            date.fromisoformat(data["card_issue_date"]),
            UUID(data["card_holder_id"]),
            CardStatus(data["card_status"]),
        )
        card.save()

        return jsonify({"message": "Card created", "card_id": str(card.card_id)}), 201

    # Endpoint to list card data
    @app.route("/card/<card_id>", methods=["GET"])
    def get_card(card_id):
        card = Card.load_from_db(UUID(card_id))

        if card is not None:
            return (
                jsonify(
                    {
                        "card_id": str(card.card_id),
                        "card_number": card.mask_card_number(),
                        "card_expire_date": card.card_expire_date,
                        "card_cvv": "***",
                        "card_issue_date": card.card_issue_date,
                        "card_holder_id": str(card.card_holder_id),
                        "card_status": card.card_status.value,
                    }
                ),
                200,
            )
        else:
            return jsonify({"message": "Card not found"}), 404

    # Endpoint to activate card
    @app.route("/cards/<card_id>/activate", methods=["PUT"])
    def activate_card(card_id):
        card_id = UUID(card_id)
        card = Card.load_from_db(card_id)
        if not card:
            return make_response(jsonify({"error": "Card not found"}), 404)
        try:
            card.activate()
            return jsonify({"status": "Card activated"})
        except ValueError as e:
            return make_response(jsonify({"error": str(e)}), 400)

    # Endpoint to block card
    @app.route("/cards/<card_id>/block", methods=["PUT"])
    def block_card(card_id):
        card_id = UUID(card_id)
        card = Card.load_from_db(card_id)
        if not card:
            return make_response(jsonify({"error": "Card not found"}), 404)
        card.block()
        return jsonify({"status": "Card blocked"})

    return app


if __name__ == "__main__":
    create_app().run(debug=False)
