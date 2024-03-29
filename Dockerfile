FROM python:2.7-stretch

MAINTAINER Antonio Ideguchi

ADD ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]
