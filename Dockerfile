FROM python:3.11.8-alpine

ENV TZ=Asia/Almaty

WORKDIR /app

# Installing netcat to check port availability
RUN apk add --no-cache netcat-openbsd

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY src ./src
COPY alembic.ini ./
COPY main.py ./

# Adding and setting up entrypoint.sh
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
CMD ["python", "main.py"]
