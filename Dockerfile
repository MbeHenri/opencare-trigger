FROM python:3.10
LABEL version="1.0"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY patient.py .
COPY server.py .

CMD [ "python", "./server.py" ]