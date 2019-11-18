FROM python:3.7
COPY ./asperathos-monitor /asperathos-monitor
WORKDIR /asperathos-monitor
COPY ./monitor.cfg ./monitor.cfg
RUN pip install setuptools tox flake8
ENTRYPOINT ./run.sh
