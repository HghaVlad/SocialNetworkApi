FROM python:3.10


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app


ENTRYPOINT ["sh", "/app/entrypoint.sh"]
