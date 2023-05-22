FROM python:3.9.1-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY  instance ./instance
COPY wsgi.py wsgi.py
COPY run.py run.py
COPY blog ./blog

EXPOSE 5000

CMD ["python", "run.py"]