import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

# Snapshot of the original in-memory data, taken before any test mutates it.
_ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory activities dict so tests don't leak state."""
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))


@pytest.fixture
def client():
    return TestClient(app)
