FROM python:3.7-alpine

RUN apk add socat gcc musl-dev
 
WORKDIR /var/www/html/uploads

COPY . .

RUN chmod +x main.py

ENTRYPOINT ["python3", "./main.py"]
