FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app app

# Copy public & private keys
COPY student_public.pem /app/
COPY instructor_public.pem /app/
COPY instructor_private.pem /app/

# Create data and cron directories
RUN mkdir -p /app/data /app/cron

# Copy cron and seed files
COPY data/cron/last_code.txt /app/cron/last_code.txt
COPY data/encrypted_seed.txt /app/data/encrypted_seed.txt
COPY data/encrypted_seed.sig /app/data/encrypted_seed.sig

EXPOSE 8080

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
