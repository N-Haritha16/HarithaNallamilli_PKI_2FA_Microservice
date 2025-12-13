FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and files
COPY app app
COPY student_public.pem .
COPY instructor_public.pem .
COPY encrypted_seed.txt .
COPY encrypted_seed.sig .

# Create data and cron directories
RUN mkdir -p /data /cron

# Copy the cron script and make it executable
COPY cron/rotate_seed.sh /cron/rotate_seed.sh
RUN chmod +x /cron/rotate_seed.sh

EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
