FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render sets $PORT automatically
ENV PORT=10000

CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "app:app"]
