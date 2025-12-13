FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY student_public.pem .
COPY instructor_public.pem .
COPY encrypted_seed.txt .
COPY encrypted_seed.sig .

RUN mkdir /data

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
