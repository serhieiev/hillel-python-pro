# lesson_08: Django. Models, Migrations, Tests.

## Home assignment

ДЗ 9. Створити Django application для отримання і створення карток

На базі домашки #7.

1. Створити модель картки
2. Створити API для створення та отримання даних картки
3. База – Postgres
4. Міграції обовʼязкові
5. Тести для API та для методів моделі, якщо у вас будуть кастомні методи.
6. API повинен бути JSON.
7. Написати метод is_valid() який повертає True якщо номер валідний і False якщо ні. Метод повинен перевітяти Luhn check.

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
python config/manage.py runserver
```

To run tests:
```bash
python manage.py test --verbosity=2
```

