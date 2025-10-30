FROM python:3.13-slim

# Install FFmpeg, PostgreSQL libs, and system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        wget \
        ca-certificates \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p media/audio_files staticfiles

# Expose port
EXPOSE 8080

# Run Django setup and Gunicorn server
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn ai_blog_app.wsgi:application --bind 0.0.0.0:$PORT --timeout 300 --workers 2 --log-file -
