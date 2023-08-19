from fastapi import FastAPI
import httpx

app = FastAPI()

RECIPE = {
    "flour": 200,  # grams per bun
    "milk": 100,  # milliliters per bun
    "sugar": 20,  # grams per bun
    "salt": 4,  # grams per bun
    "eggs": 2,  # count per bun
}


@app.get("/buns")
async def calculate_buns():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/ingredients")
        ingredients = response.json()

    buns = min(ingredients[key] // value for key, value in RECIPE.items())

    if buns == 0:
        return {"error": "Not enough ingredients even for one bun. Please resupply!"}

    return {"buns": buns}
