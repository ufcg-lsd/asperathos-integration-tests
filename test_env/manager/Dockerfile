FROM python:2.7
COPY ./asperathos-manager /asperathos-manager
WORKDIR /asperathos-manager
COPY ./broker.cfg ./broker.cfg
RUN pip install setuptools tox flake8
RUN pip install -r requirements.txt
ENTRYPOINT ./run.sh
