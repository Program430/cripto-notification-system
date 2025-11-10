import logging

import pytest


@pytest.fixture(scope="session", autouse=True)
def disable_logs():
    previous_disable_level = logging.root.manager.disable

    logging.disable(logging.CRITICAL)

    yield

    logging.disable(previous_disable_level)
