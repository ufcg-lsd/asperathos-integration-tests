FROM python:3.7
COPY ./asperathos-monitor /asperathos-monitor
WORKDIR /asperathos-monitor
COPY ./monitor.cfg ./monitor.cfg
RUN pip3 install setuptools tox flake8
RUN pip3 install -r requirements.txt
ENTRYPOINT python3.7 run.py
