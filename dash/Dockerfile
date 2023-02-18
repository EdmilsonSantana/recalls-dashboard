FROM python:3.10-slim-buster

EXPOSE 8050/tcp

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./app.py"]