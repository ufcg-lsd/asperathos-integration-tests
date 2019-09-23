FROM python:3.7
COPY ./asperathos-visualizer /asperathos-visualizer
WORKDIR /asperathos-visualizer
COPY ./visualizer.cfg ./visualizer.cfg
RUN pip install setuptools tox flake8
ENTRYPOINT ./run.sh
