FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt ./

RUN apk add build-base supervisor

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["/usr/bin/supervisord", "-c", "/app/supervisord.conf"]
