# 1. Base Image: Lightweight Debian Linux with Python 3.12
FROM python:3.12-slim

# 2. Environment Flags:
# Stop Python from generating .pyc files (saves space)
ENV PYTHONDONTWRITEBYTECODE=1
# Force Python to flush logs immediately to stdout/stderr (crucial for Railway logs)
ENV PYTHONUNBUFFERED=1

# 3. Work Directory: Create and enter /app
WORKDIR /app

# 4. Dependency Caching:
# Copy ONLY requirements.txt first so Docker caches installed packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Project Code:
# Copy the rest of the project into /app
COPY . .

# 6. Django Path Setup:
# In your project, manage.py is inside the 'core/' folder.
# We move into /app/core so manage.py and wsgi can be found.
WORKDIR /app/core

# 7. Port Binding for Railway:
# Expose port 8000 (documentation)
EXPOSE 8000

# 8. Run Migrations & Start the Server:
# Railway provides a dynamic $PORT environment variable.
# Automatically runs database migrations, then starts the production WSGI server.
CMD ["sh", "-c", "python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]