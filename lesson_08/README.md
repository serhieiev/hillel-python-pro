# lesson_08: Робота с PostgresSQL. ООП. SOLID.

## Home assignment

ДЗ 7. На базі домашки #5 зробити наступнеЖ

1. Необхідно підключити модель до PostgresSQL замість SQLite.
2. Створити flask application.
3. Створити методи створення та оримання картки.
4. Без ORM, чистий SQL
5. Міграції робити не обовʼязково. Можна створити таблиці руками.


Тести – обовʼязкові. Юніт тести для моделі, інтеграційні тести для flask application.

Рішення залити на github як PULL REQUEST

## Solution

To create postgresql `cards` table, execute:

```sql
CREATE TABLE cards (
    card_id UUID PRIMARY KEY,
    card_number TEXT NOT NULL,
    card_expire_date DATE NOT NULL,
    card_cvv TEXT NOT NULL,
    card_issue_date DATE NOT NULL,
    card_holder_id UUID NOT NULL,
    card_status CardStatus NOT NULL
);
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

