FROM python:3.10-slim-buster

EXPOSE 8501/tcp

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.maxUploadSize=1028"]