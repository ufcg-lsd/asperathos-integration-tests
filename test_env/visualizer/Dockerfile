FROM python:2.7
COPY ./asperathos-visualizer /asperathos-visualizer
WORKDIR /asperathos-visualizer
COPY ./visualizer.cfg ./visualizer.cfg
RUN pip install setuptools tox flake8
RUN pip install -r requirements.txt
ENTRYPOINT ./run.sh
