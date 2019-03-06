import requests
from time import sleep
from helpers import wait_for_grafana_url_generation, create_job, stop_job, MANAGER_URL, VISUALIZER_URL
from helpers.fixtures import job_payload


def test_create_job(job_payload):
    """ Tests if a Job is being created successfully
            Arguments:
                job_payload {dict} -- A pytest fixture providing the Job payload to be sent to Asperathos
            Returns:
                None
    """
    response = requests.post(MANAGER_URL + '/submissions', json=job_payload)
    response_payload = response.json()
    assert response.ok
    assert response_payload
    stop_job(manager_url=MANAGER_URL, job_id=response_payload.get('job_id'))


def test_visualize_grafana():
    """ Tests if the Grafana URL is being generated successfully
            Arguments:
                None
            Returns:
                None
    """
    job_id = create_job(MANAGER_URL)
    grafana_url = wait_for_grafana_url_generation(VISUALIZER_URL, job_id)
    assert requests.get(grafana_url).ok
    stop_job(manager_url=MANAGER_URL, job_id=job_id)
