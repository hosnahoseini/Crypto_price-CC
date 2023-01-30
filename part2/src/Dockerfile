FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENV REDIS_PASSWORD="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81"

CMD ["python", "/app/main.py"]
