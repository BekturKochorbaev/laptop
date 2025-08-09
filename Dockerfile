FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install psycopg2-binary
RUN pip install gunicorn
RUN pip install setuptools
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "-b", "0.0.0.0:8000", "laptop.wsgi:application"]
