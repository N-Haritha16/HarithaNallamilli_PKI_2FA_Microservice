FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app app

# Copy public keys
COPY student_public.pem .
COPY instructor_public.pem .

# Create data directory inside container (optional)
RUN mkdir -p /data /cron
COPY cron/task_code.txt /cron/task_code.txt

# Copy seed files from local project data folder
COPY data/encrypted_seed.txt /app/data/seed.txt
COPY data/encrypted_seed.sig /app/data/seed.sig

EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
