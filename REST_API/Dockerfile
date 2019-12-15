FROM python:3

WORKDIR /rest
COPY . /rest

ENV API_ID = 1234
ENV API_HASH = 1234

RUN pip install -r requirements.txt

CMD python3 botAPI.py
