import requests
import json
import subprocess
import logging

from time import sleep
from os import environ
from subprocess import PIPE
from datetime import datetime

global_enabled = False

DOCKER_HOST = environ['DOCKER_HOST_URL']
MANAGER_URL = "http://{}:1500".format(DOCKER_HOST)
CONTROLLER_URL = "http://{}:1502".format(DOCKER_HOST)
MONITOR_URL = "http://{}:5001".format(DOCKER_HOST)
VISUALIZER_URL = "http://{}:5002".format(DOCKER_HOST)


def wait_until_manager_is_up(manager_url, max_wait_time=1000, max_tries=50):
    delta = max_wait_time / max_tries
    error_count = 0
    for _ in range(max_tries):
        sleep(delta)
        try:
            response = requests.get(manager_url + '/healthz')
            if response.ok:
                return error_count
        except:
            print("Could not contact manager. Trying again")
            error_count += 1
            # url = response.json().get('url')
            # if url != "URL not generated!":
            #    return url
    raise Exception("Max tries to contact manager exceeded.")


def wait_for_grafana_url_generation(visualizer_url, job_id, max_wait_time=120, max_tries=10):
    """ Waits for a defined time for asperathos to generate the Grafana URL.
            Arguments:
                visualizer_url {string} -- The URL from the Asperathos Visualizer
                job_id {string} -- Job id generated when the job is submitted
                max_wait_time {int} -- Maximum time, in seconds, to be waited
                max_tries {int} -- Maximum times this function will try to get the URL
            Returns:
                url {string} -- Grafana URL
            Raises:
                Exception -- When max_tries is reached without success
    """
    delta = max_wait_time / max_tries
    for _ in range(max_tries):
        sleep(delta)
        response = requests.get(visualizer_url + '/visualizing/{}'.format(job_id))
        if response.ok:
            url = response.json().get('url')
            if url != "URL not generated!":
                return url
    raise Exception("Max tries to get generated URL exceeded.")

def wait_for_job_complete(manager_url, job_id, max_wait_time=120, max_tries=10):
    """ Waits for a defined time for a job to be completed.
            Arguments:
                manager_url {string} -- The URL from the Asperathos Manager
                job_id {string} -- Job id generated when the job is submitted
                max_wait_time {int} -- Maximum time, in seconds, to be waited
                max_tries {int} -- Maximum times this function will try to get the URL
            Returns:
                url {string} -- Grafana URL
            Raises:
                Exception -- When max_tries is reached without success
    """
    delta = max_wait_time / max_tries
    for _ in range(max_tries):
        sleep(delta)
        response = requests.get(manager_url + '/submissions/{}'.format(job_id))
        if response.ok:
            status = response.json().get('status')
            print("status:",status)
#            if status == "completed":# and response.json().get('final_replicas'):
            if status == "finished":# and response.json().get('final_replicas'):
                    return True

    raise Exception("Max tries for job to be completed exceeded.")

def create_job(manager_url, payload):
    """ Submits a job to Asperathos
            Arguments:
                manager_url {string} -- THe URL from Asperathos Manager
                payload {int} -- the id for the choosen payload
            Returns:
                job_id {string} -- The Job identifier
    """
    job_payload = get_job_payload(payload)
    response = requests.post(manager_url + '/submissions', json=job_payload)
    response_payload = response.json()
    job_id = response_payload.get('job_id')
    return job_id


def stop_job(manager_url, job_id):
    #TODO: discuss a better way of stopping jobs or solve the manager's unwanted behavior
    # of not being able to stop a job until the Redis queue is populated
    """ Stops a running job
            Arguments:
                manager_url {string} -- THe URL from Asperathos Manager
                job_id {string} -- Job id generated when the job is submitted
            Returns:
                None
    """
    requests.put(manager_url + '/submissions/' + job_id, json={
        "enable_auth": False
    })


def get_job_payload(id):
    """ Retrieves JSON payload of the job from the assets folder
            Arguments:
                None
            Returns:
                Job's JSON payload {dict}
    """
    payload_path = "assets/payload" + str(id) + ".json"
    with open(payload_path, 'r') as f:
        return json.loads(f.read())


def get_jobs(manager_url):
    return requests.get(manager_url + "/submissions").json()


def delete_job(manager_url, job_id):
    requests.delete(manager_url + "/submissions/{}".format(job_id),
                    json={
                          "enable_auth": False
                         })


def get_manager_container_id():
    """ Retrieves manager container id
            Arguments:
                None
            Returns:
                Manager container id
        """
    docker_command = 'docker container ls -q -f name=manager'
    id_ = subprocess.check_output(docker_command, shell=True).split()[0]
    return id_.decode()


def restart_container(container_id):
    docker_command = 'docker restart {} && sleep 1m'.format(container_id)
    subprocess.check_output(docker_command, shell=True)


def setup_asperathos():
    subprocess.run(["docker-compose", "up", "-d", "--force-recreate"], cwd="test_env", check=True, stdout=PIPE, stderr=PIPE)
    wait_until_manager_is_up(MANAGER_URL)


def teardown_asperathos():
    subprocess.run(["docker-compose", "down"], cwd="test_env", check=True, stdout=PIPE, stderr=PIPE)
    subprocess.run(["kubernetes/asperathos_cleanup.sh", "kubernetes/config"], check=True, stdout=PIPE, stderr=PIPE)

class Log:
    def __init__(self, name, output_file_path):
        self.logger = logging.getLogger(name)
        if not len(self.logger.handlers):
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            self.logger.addHandler(handler)
            handler = logging.FileHandler(output_file_path)
            self.logger.addHandler(handler)
            self.logger.propagate = False

    def log(self, text):
        if global_enabled:
            self.logger.info(text)

def enable():
    global global_enabled
    global_enabled = True

def disable():
    global global_enabled
    global_enabled = False

def configure_logging(logging_level="INFO"):
    levels = {"CRITICAL": logging.CRITICAL, "DEBUG": logging.DEBUG,
              "ERROR": logging.ERROR, "FATAL": logging.FATAL,
              "INFO": logging.INFO, "NOTSET": logging.NOTSET,
              "WARN": logging.WARN, "WARNING": logging.WARNING
              }
    logging.basicConfig(level=levels[logging_level])

def get_logger():
    configure_logging()
    enable()
    return Log("log", "integration.log")


