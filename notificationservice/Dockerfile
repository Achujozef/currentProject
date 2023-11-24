FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y gcc && pip install --no-cache-dir -r requirements.txt

EXPOSE 8005

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8005 & python consumer.py"]
