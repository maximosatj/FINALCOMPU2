FROM python:3.10

RUN groupadd -r example && useradd -r -g example employee

USER employee

WORKDIR /app

COPY server.py client.py /app/

CMD ["python", "server.py"]
