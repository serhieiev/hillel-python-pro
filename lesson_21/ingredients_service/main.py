from fastapi import FastAPI

app = FastAPI()

ingredients = {
    "flour": 1000,  # grams
    "milk": 500,  # milliliters
    "sugar": 100,  # grams
    "salt": 20,  # grams
    "eggs": 10,  # count
}


@app.get("/ingredients")
def get_ingredients():
    return ingredients
