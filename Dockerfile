FROM python:latest

ADD pythonArbitrage.py /home
COPY arbitrage /home/arbitrage
COPY democlient /home/democlient
COPY test /home/test

RUN pip install shrimpy-python

CMD [ "python", "/home/pythonArbitrage.py" ]