FROM python:3.11-slim
LABEL authors="dikin"

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 blog_project.asgi:application"]