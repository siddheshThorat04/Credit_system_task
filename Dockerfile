# Dockerfile
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files (if using)
RUN python manage.py collectstatic --noinput

# Run app
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
