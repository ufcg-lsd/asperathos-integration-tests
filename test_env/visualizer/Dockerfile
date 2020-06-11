FROM python:3.7
COPY ./asperathos-visualizer /asperathos-visualizer
WORKDIR /asperathos-visualizer
COPY ./visualizer.cfg ./visualizer.cfg
RUN pip3 install setuptools tox flake8
RUN pip3 install -r requirements.txt
ENTRYPOINT python3.7 run.py
