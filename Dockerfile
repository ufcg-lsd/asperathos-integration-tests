FROM integration_tests_base
RUN apt install docker-compose -y
COPY . /integration-tests/
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && chmod +x ./kubectl && mv ./kubectl /bin
WORKDIR /integration-tests/
RUN pip install -r requirements.txt
ENTRYPOINT ./build_and_run_tests.sh
