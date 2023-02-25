FROM python:3.10

WORKDIR /game/

COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . ./

CMD python3 console_trucker.py
