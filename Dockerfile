FROM python:3
LABEL version="1.0"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY patient.py patient.py
COPY server.py server.py

CMD [ "python", "./server.py" ]