FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /music_insights

COPY ./music_insights/requirements.txt/. .
COPY ./music_insights/requirements-lint.txt/. .
COPY ./music_insights/requirements-dev.txt/. .

RUN pip install -r requirements-dev.txt
