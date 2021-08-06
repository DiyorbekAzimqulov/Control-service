FROM python:latest


ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code


COPY requirements.txt .
COPY attendance .
COPY media .
COPY API .
COPY manage.py .
COPY db.sqlite3 .
RUN pip install cmake
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

