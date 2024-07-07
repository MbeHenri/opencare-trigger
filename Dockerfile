FROM python:3.10
LABEL version="1.0"

WORKDIR /app

COPY . ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./server.py" ]
