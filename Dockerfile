FROM python:3.8-alpine

LABEL maintainer="Ztj <ztj1993@gmail.com>"

ENV MYSQL_HOST="localhost"
ENV MYSQL_PORT="3306"
ENV MYSQL_USER="root"
ENV MYSQL_PASSWORD=""
ENV MYSQL_CHARSET="utf8mb4"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]

CMD ["--help"]
