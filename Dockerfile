FROM python:3.10


ENV  PYTHONBUFFERED = 1


WORKDIR /app

ADD . .


RUN pip install -r requirments.txt


EXPOSE 8080

CMD python manage.py runserver 0.0.0.0:8080