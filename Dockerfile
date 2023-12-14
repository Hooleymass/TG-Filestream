FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt ./

RUN apk add build-base
# Install dependencies for psutil
RUN apk --no-cache add gcc python3 linux-headers

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3","-m","biisal"]
