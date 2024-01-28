FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip3 install pip --upgrade --no-cache-dir
RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
