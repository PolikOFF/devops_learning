FROM python:3.10-slim

WORKDIR /app

COPY check_site.py .

RUN pip install --no-cache-dir psycopg2-binary

CMD ["python", "check_site.py"]
