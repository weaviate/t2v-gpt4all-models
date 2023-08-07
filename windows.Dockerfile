FROM python:3.11-windowsservercore

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN python download.py

CMD ["uvicorn app:app --host 0.0.0.0 --port 8080"]
