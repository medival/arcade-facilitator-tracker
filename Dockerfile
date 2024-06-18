FROM python:3.11.9-bullseye

ENV TZ="Asia/Jakarta"

RUN apt update 

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt

COPY templates /app/templates/
COPY app.py /app/
COPY wsgi.py /app/

CMD ["gunicorn", "--bind","0.0.0.0:5000", "wsgi:app", "--timeout", "600", "--workers", "5", "--worker-connections=1000"]