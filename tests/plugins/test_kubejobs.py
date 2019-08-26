import requests
import pytest
import subprocess
from time import sleep
from helpers import wait_for_grafana_url_generation, create_job
from helpers import stop_job, MANAGER_URL, VISUALIZER_URL, get_jobs, delete_job
from helpers import restart_container
from helpers.fixtures import job_payload, manager_container_id


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


@pytest.mark.last
def test_persistence_works(manager_container_id):
    """ Tests if Job persistence is working properly
    when manager is restarted
            Arguments:
                None
            Returns:
                None
    """
    # This test is here to ensure there will be more than 0 jobs registered
    jobs = get_jobs(MANAGER_URL)
    n_jobs = len(jobs)
    assert n_jobs > 0

    restart_container(manager_container_id)
    assert n_jobs == len(get_jobs(MANAGER_URL))

    delete_job(MANAGER_URL, list(jobs.keys())[0])
    assert len(get_jobs(MANAGER_URL)) < n_jobs
