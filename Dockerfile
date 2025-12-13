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

# Create required directories
RUN mkdir -p /data

# Copy encrypted seed and signature to /data (MANDATORY)
COPY encrypted_seed.txt /data/seed.txt
COPY encrypted_seed.sig /data/seed.sig

EXPOSE 8000

# Start API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
