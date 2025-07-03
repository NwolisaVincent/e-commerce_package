FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirments.txt

COPY ..


RUN python manage.py collectstatic --noinput

CMD gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT
