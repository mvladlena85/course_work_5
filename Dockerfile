FROM python:3.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY data data
COPY templates templates
COPY . .
CMD gunicorn wsgi:app -b 0.0.0.0:80


