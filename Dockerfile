FROM python:3.9-slim

RUN apt-get update && apt-get install -y speedtest-cli

RUN pip install psycopg2-binary schedule

COPY index.py /app/index.py

CMD ["python", "/app/index.py"]