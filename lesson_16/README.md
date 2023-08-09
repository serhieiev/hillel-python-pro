# lesson_16: Celery. Django Celery

## Home assignment

ДЗ 13. Celery tasks
1. Create an Asynchronous Method: Based on previous assignments, make the `activate` method asynchronous. Before activating the card, wait for 2 minutes. Writing a test for this is not obligatory, but if you figure out how, you'll get +5 bonus points on any homework.
2. Freezing Cards: Use `django-celery-beat` to create a task that freezes cards with an expiry date greater than today's date.

## Solution

### Database Setup

First, you'll need to perform migrations to reflect the model changes into your database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Encryption Key Generation

Generate an encryption key using the following commands:
```python
python3
>>> from cryptography.fernet import Fernet
>>> key = Fernet.generate_key()
>>> print(key)
```

### Environment Configuration

The connection to the PostgreSQL database and the `SECRET_KEY` is managed via a `.env` file. Follow these steps to create and configure the `.env` file:

To create `.env` file, execute the next command in the project root dir:
```bash
touch .env
```

Edit the `.env File:` Open the `.env` file and add the environment variables listed below with the appropriate values:
```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
SECRET_KEY=
```

### Redis Setup with Docker

Create a new network::
```bash
docker network create redis-network
```
Start Redis::
```bash
docker run -d --name redis-broker --network redis-network -p 6379:6379 redis
```

Start Redis UI in the same Docker network:
```bash
docker run -it --rm --name redis-commander --network redis-network -p 8081:8081 --env REDIS_HOSTS=local:redis-broker:6379 rediscommander/redis-commander:latest
```

### Celery Configuration

Start Celery Worker:
```bash
celery -A config  worker -l INFO
```

Start Celery Beat:
```bash
celery -A config beat -l DEBUG
```

### Django Server

To run the Django server, use the following command:
```bash
python manage.py runserver
```

Run the tests with the following command:
```bash
python manage.py test --verbosity=2
```

