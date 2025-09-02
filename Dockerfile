FROM python:alpine3.22

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app

COPY . /app

CMD [ "python", "/app/flask_website.py" ]