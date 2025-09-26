# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port your app runs on (Render expects 10000+)
EXPOSE 10000

# Start the application (update if your app entry is different)
CMD ["python", "app.py"]
