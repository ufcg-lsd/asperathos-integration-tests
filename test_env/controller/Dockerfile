FROM python:3.7
COPY ./asperathos-controller/ /asperathos-controller/
WORKDIR /asperathos-controller
COPY ./controller.cfg ./controller.cfg
RUN pip3 install setuptools tox flake8
RUN pip3 install -r requirements.txt 
ENTRYPOINT python3.7 run.py
