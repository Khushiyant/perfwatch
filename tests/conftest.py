import pytest


@pytest.fixture
def dummy_function():
    for _ in range(10000):
        pass
