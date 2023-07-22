# lesson_11: Django auth. Getting started with the Django REST Framework.

## Home assignment

ДЗ 11. Створити DRF додаток для карток

На базі попередньої домашки переписати код з використанням django rest framework.

1. Додати до моделі картки поле owner яке повинно бути моделлю django User.
2. Додати до моделі опціональне імʼя картки.
3. Створити ендпоінти які будуть:
- Повертати усі картки поточного користувача
- Повертати одну картку по ID. Але треба перевірити, що вона доступна користувачу.
- Створювати картки для поточного користувача
- Оновлювати картку. (подумайте які поля може оновлювати користувач)
- Заморожувати картку (чи потрібен вам новий статус?)
- Ре-активутати картку після заморозки

Написати тести для всіх ендпоінтів.

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

