FROM python:3-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .

RUN pip install -r requirements.txt \
    && pip install --no-cache-dir gunicorn

COPY . .

ENV FLASK_APP=main.py

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
