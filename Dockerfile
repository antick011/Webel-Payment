FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render sets $PORT automatically
# You can remove ENV PORT=10000 if you want to use Render's default
# ENV PORT=10000

CMD gunicorn -b 0.0.0.0:$PORT app:app
