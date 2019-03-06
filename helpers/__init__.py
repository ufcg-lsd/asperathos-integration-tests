import requests
from time import sleep
import json
from os import environ

DOCKER_HOST = environ['DOCKER_HOST_URL']
MANAGER_URL = "http://{}:1500".format(DOCKER_HOST)
CONTROLLER_URL = "http://{}:5000".format(DOCKER_HOST)
MONITOR_URL = "http://{}:5001".format(DOCKER_HOST)
VISUALIZER_URL = "http://{}:5002".format(DOCKER_HOST)


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


def create_job(manager_url):
    """ Submits a job to Asperathos
            Arguments:
                manager_url {string} -- THe URL from Asperathos Manager
            Returns:
                job_id {string} -- The Job identifier
    """
    job_payload = get_job_payload()
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


def get_job_payload():
    """ Retrieves JSON payload of the job from the assets folder
            Arguments:
                None
            Returns:
                Job's JSON payload {dict}
    """
    with open("assets/payload.json", 'r') as f:
        return json.loads(f.read())
