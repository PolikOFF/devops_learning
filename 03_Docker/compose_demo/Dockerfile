FROM python:3.10-slim

WORKDIR /app

COPY check_site.py .

RUN pip install --no-cache-dir urllib3

CMD ["python", "check_site.py"]
