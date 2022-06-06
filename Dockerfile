FROM python:3.10.4-buster
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

CMD ["uwsgi","--ini", "/app/uwsgi.ini"]