from flask import Flask, request

from utils import get_currency_exchange_rate, get_pb_exchange_rate

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p><b>Hello, World!</b></p>"


@app.route("/rates", methods=["GET"])
def get_rates():
    currency_a = request.args.get("currency_a", default="USD")
    currency_b = request.args.get("currency_b", default="UAH")
    result = get_currency_exchange_rate(currency_a, currency_b)
    return result


@app.route("/rates_pb", methods=["GET"])
def get_pb_rates():
    convert_currency = request.args.get("convert_currency", default="USD")
    bank = request.args.get("bank", default="NBU")
    rate_date = request.args.get("rate_date", default="01.11.2022")
    result = get_pb_exchange_rate(convert_currency, bank, rate_date)
    return result


# Test Queries
# http://127.0.0.1:5000/rates_pb?rate_date=22.08.2022&bank=nationalbank
# http://127.0.0.1:5000/rates_pb?rate_date=2022-08-22&bank=nbu
# http://127.0.0.1:5000/rates_pb?rate_date=22-08-2022&bank=privatbank
# http://127.0.0.1:5000/rates_pb?rate_date=8.22.2022&bank=privatbank
