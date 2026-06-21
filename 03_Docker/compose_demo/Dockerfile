FROM python:3.10-slim

WORKDIR /app

COPY check_site.py .
COPY check_site_ci.py .

RUN pip install --no-cache-dir psycopg2-binary

CMD ["python", "check_site.py"]
