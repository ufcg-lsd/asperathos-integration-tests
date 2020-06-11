import pytest
import subprocess
#import logger

from helpers import get_job_payload, get_manager_container_id
from helpers import wait_until_manager_is_up, MANAGER_URL
from helpers import setup_asperathos, teardown_asperathos, get_logger
from subprocess import PIPE
#from logger import Log

@pytest.fixture
def job_payload():
        """ Pytest fixture to retrieve the job payload from assets folder
            Arguments:
                None
            Returns:
                Job payload
        """
        return get_job_payload(1)

@pytest.fixture
def manager_container_id():
    """ Pytest fixture to retrieve manager container id
            Arguments:
                None
            Returns:
                Manager container id
        """
    return get_manager_container_id()

#def _setup_asperathos():
#    subprocess.run(["docker-compose", "up", "-d", "--force-recreate"], cwd="test_env", check=True, stdout=PIPE, stderr=PIPE)
#    wait_until_manager_is_up(MANAGER_URL)

#def _teardown_asperathos():
#    subprocess.run(["docker-compose", "down"], cwd="test_env", check=True, stdout=PIPE, stderr=PIPE)
#    subprocess.run(["kubernetes/asperathos_cleanup.sh", "kubernetes/config"], check=True, stdout=PIPE, stderr=PIPE)

@pytest.fixture
def setup_and_teardown_asperathos():
    setup_asperathos()
    yield 0
    teardown_asperathos()

@pytest.fixture
def logger():
    return get_logger()
#    configure_logging()
#    enable()
#    return Log("log", "integration.log")
#    return logger.log("log", "integration.log")
