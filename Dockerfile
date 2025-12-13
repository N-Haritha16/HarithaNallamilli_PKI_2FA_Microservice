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

# Create data directory
RUN mkdir -p /data

# Copy seed files
COPY encrypted_seed.txt /data/seed.txt
COPY encrypted_seed.sig /data/seed.sig

EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
