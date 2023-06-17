# lesson_06: Поглиблення у тести. Монолітна, мікросервісна архітектура. MVC.

## Home assignment

ДЗ 5. Написати модель банківської картки та методи зберіганні моделі у базі данних

Модель повинна мати наступні поля:

- Номер картки - PAN 16 цифр
- Дата закінчення сроку дії у форматі місяць/рік
- CVV код 3 цифри
- Дата видачі - дата
- ID власника - UUID (розібрати що таке UUID самостійно)
- Статус картки (нова, активна, заблокована). Може бути рядком.
- Реалізувати збереження та читання даних з sqlite.

- Реалізувати методи моделі для зміни активації картки та блокування. Заблокована картка не може бути активована.

- Покрити тестами логіку активації, блокування та роботи з БД.



Матеріали по фікстурам баз даних https://medium.com/@geoffreykoh/fun-with-fixtures-for-database-applications-8253eaf1a6d



Максимум 99 балів за завдання. 100 балів отримує той, хто з першого разу додасть до моделі якісь фічі з безпеки даних. Фічі з безпеки – необовʼязкове завдання.



Здати як лінку на репозиторій на github.



Acceptance criteria (-10 балів за невиконання):

Модель має усі перелічені поля
Може бути збережена у БД
Покриття тестами
Не можна використовувати ORM (SqlAlchemi наприклад) тільки чистий sql.

## Solution

To create sqlite3 `cards.db` execute:

```python
python3
>>> import sqlite3
>>> conn = sqlite3.connect('cards.db')
>>> c = conn.cursor()
>>> c.execute('''
CREATE TABLE Cards (
card_id TEXT PRIMARY KEY,
card_number TEXT NOT NULL,
card_expire_date TEXT NOT NULL,
card_cvv TEXT NOT NULL,
card_issue_date TEXT NOT NULL,
card_holder_id TEXT NOT NULL,
card_status INTEGER NOT NULL
)
''')
>>> conn.commit()
>>> conn.close()
```

To generate encryption key
```python
python3
>>> from cryptography.fernet import Fernet
>>> key = Fernet.generate_key()
>>> print(key)
```

To set environment variables in the terminal execute:
```bash
export SECRET_KEY=key
```
