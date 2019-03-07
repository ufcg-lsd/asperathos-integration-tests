import pytest
from helpers import get_job_payload

@pytest.fixture
def job_payload():
        """ Pytest fixture to retrieve the job payload from assets folder
            Arguments:
                None
            Returns:
                None
        """
        return get_job_payload()

