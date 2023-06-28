FROM python:3.11.4-bullseye

COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./src/ .

RUN bash -c "mkdir -p ./util/data"

CMD ["python3", "main.py"]