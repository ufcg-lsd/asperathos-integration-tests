FROM python:3.7
COPY ./asperathos-manager /asperathos-manager
WORKDIR /asperathos-manager
COPY ./broker.cfg ./broker.cfg
RUN pip3 install setuptools tox flake8
RUN pip3 install -r requirements.txt
ENTRYPOINT python3.7 run.py
