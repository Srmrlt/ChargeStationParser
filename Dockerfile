FROM python:3.11.8-alpine

ENV TZ=Asia/Almaty

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY src ./src
COPY main.py ./

ENTRYPOINT ["python", "main.py"]
