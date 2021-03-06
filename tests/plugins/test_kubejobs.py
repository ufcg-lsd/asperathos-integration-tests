import requests
import pytest
import subprocess
from datetime import datetime

from helpers import wait_for_grafana_url_generation, create_job
from helpers import stop_job, MANAGER_URL, VISUALIZER_URL, get_jobs, delete_job
from helpers import restart_container, wait_for_job_complete
from helpers.fixtures import job_payload, manager_container_id


def test_create_job(job_payload):
    """ Tests if a Job is being created successfully
            Arguments:
                job_payload {dict} -- A pytest fixture providing the Job
                                      payload to be sent to Asperathos
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
    job_id = create_job(MANAGER_URL, 1)
    grafana_url = wait_for_grafana_url_generation(VISUALIZER_URL, job_id)
    assert requests.get(grafana_url).ok
    stop_job(manager_url=MANAGER_URL, job_id=job_id)

def test_controller_scales_up():
    """ Tests if the Controlling is able to scale
        Arguments:
            None
        Returns:
            None
    """
    INITIAL_REPLICAS = 1
    job_id = create_job(MANAGER_URL, 2)
    wait_for_job_complete(MANAGER_URL, job_id, max_wait_time=180)
    detailed_report = requests.get(MANAGER_URL + '/submissions/{}/report'\
                      .format(job_id))
    data = detailed_report.json()
    assertion = any(data[time]['replicas'] > INITIAL_REPLICAS for time in data)
    assert assertion
    stop_job(manager_url=MANAGER_URL, job_id=job_id)

def test_controller_scales_down():
    """ Tests if the Controlling is able to scale
        Arguments:
            None
        Returns:
            None
    """
    INITIAL_REPLICAS = 10
    job_id = create_job(MANAGER_URL, 3)
    wait_for_job_complete(MANAGER_URL, job_id, max_wait_time=180)
    detailed_report = requests.get(MANAGER_URL + '/submissions/{}/report'\
                      .format(job_id))
    data = detailed_report.json()
    assertion = any(data[time]['replicas'] < INITIAL_REPLICAS for time in data)
    assert assertion
    stop_job(manager_url=MANAGER_URL, job_id=job_id)

def test_monitor_report_matches_detailed():
    """ Tests if the metrics in the
        simple report matches with the detailed one.
    Arguments:
        None
    Returns:
        None
    """
    job_id = create_job(MANAGER_URL, 3)
    wait_for_job_complete(MANAGER_URL, job_id, max_wait_time=180)
    submission_url = MANAGER_URL + '/submissions/{}'.format(job_id)
    report_url = submission_url + "/report" 
    monitor = requests.get(submission_url).json()   
    detailed = requests.get(report_url).json()


    monitor_max_error,monitor_max_error_time = monitor['max_error']
    monitor_min_error,monitor_min_error_time = monitor['min_error']
    monitor_last_error,monitor_last_error_time = monitor['final_error']

    detailed_report_max_error = detailed[monitor_max_error_time]['error']
    assert detailed_report_max_error == monitor_max_error

    detailed_report_max_error = detailed[monitor_min_error_time]['error']
    assert detailed_report_max_error == monitor_min_error

    date_format = "%Y-%m-%dT%H:%M:%SZ"
    last_date = datetime.strptime(monitor_last_error_time,date_format)
    dates = detailed.keys()
    assertion = all(datetime.strptime(date,date_format) <= last_date\
                    for date in dates)
    assert assertion

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
