# lesson_12: Django. Templates. Admin.

## Home assignment

ДЗ 10. Створити HTML view для карток

Використовуючи код ДЗ з заняття #11 створити HTML view для:

1. Відображення карток.
2. Форма для створення карток.
3. Додати картки в django admin.
4. Покрити тестами

## Solution

Perform migrations to reflect the model into your database:

```bash
python manage.py makemigrations
python manage.py migrate
```

To generate encryption key:
```python
python3
>>> from cryptography.fernet import Fernet
>>> key = Fernet.generate_key()
>>> print(key)
```

Connection to the Postgresql DB and `SECRET_KEY` are handled via `.env` file.

To create `.env` file, execute the next command in the project root dir:
```bash
touch .env
```

After that adjust `.env` file with environment variables listed below and you values:
```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
SECRET_KEY=
```

To run Django server:
```bash
python manage.py runserver
```

To run tests:
```bash
python manage.py test --verbosity=2
```

