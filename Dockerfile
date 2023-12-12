FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt ./

RUN apk add build-base

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
 
EXPOSE 8080
 
CMD ["gunicorn", "--bind" , ":8080", "--workers", "2", "app:app"]
