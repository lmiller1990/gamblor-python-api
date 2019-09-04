FROM python:alpine
WORKDIR /app
COPY requirements.txt /app
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

COPY . /app
CMD ["python", "run.py"]
