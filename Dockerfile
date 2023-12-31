FROM python:3.11.4-bullseye

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

RUN bash -c "mkdir -p ./storage/files"

CMD ["python3", "./src/main.py"]