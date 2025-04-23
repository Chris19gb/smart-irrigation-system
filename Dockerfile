FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "src/app.py", "--server.port=8080", "--server.enableCORS=false"]
