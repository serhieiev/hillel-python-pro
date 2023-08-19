# lesson_21: Microservices architecture

## Home assignment
Using any asynchronous web framework, create 2 microservices.

1. The first service should "store" data on the remaining ingredients for making buns and return them via a GET request.
2. The second service should be able to calculate the number of buns that can be baked using data from the first service.
3. Cover both services with tests.
4. Upload to GitHub.

No need to implement database connection, migrations, etc. You can return random or static data for ease of implementation.

## Solution

Run the services:

```bash
uvicorn ingredients_service.main:app --host 0.0.0.0 --port 8000 --reload
uvicorn buns_service.main:app --host 0.0.0.0 --port 8001 --reload
```

Run the tests:

```bash
pytest ingredients_service/tests.py
pytest buns_service/tests.py
```