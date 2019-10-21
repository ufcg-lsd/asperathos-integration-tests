import pytest

from helpers import get_job_payload, get_manager_container_id

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
