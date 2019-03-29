FROM integration_tests_base
RUN apt install docker-compose -y
COPY . /integration-tests/
WORKDIR /integration-tests/
RUN pip install -r requirements.txt
ENTRYPOINT cd test_env && ./build.sh && docker-compose up -d && sleep 2m && cd .. && tox
