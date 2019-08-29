import pytest
from clients import ClientSub


@pytest.fixture(scope='session')
def sub():
    return ClientSub()
