FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
RUN mkdir /staticfiles
RUN python manage.py collectstatic --noinput --clear
CMD gunicorn yapdns.wsgi:application -w 2 -b 0.0.0.0:8000
