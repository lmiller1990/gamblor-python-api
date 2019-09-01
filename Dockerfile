FROM python:3.7-alpine
COPY . /app
 
RUN apk update && apk add python3-dev postgresql-dev gcc musl-dev
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["run.py"]
