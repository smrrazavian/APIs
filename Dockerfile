FROM python:3.10.0-alpine
RUN addgroup app && adduser -S -G app app
USER app
WORKDIR /app/
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD uvicorn main:app --reload