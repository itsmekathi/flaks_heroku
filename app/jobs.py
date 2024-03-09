"""Adding tasks on app startup."""

from .extensions import scheduler
import requests, os

@scheduler.task(
    "interval",
    id="poll_website",
    seconds=10,
    max_instances=1
)
def poll_website():
    """Pool website every 10 seconds so that it remains active
    """
    print("Pooling website!")  # noqa: T001
    url = os.environ.get('HEALTH_CHECK_ENDPOINT_URL') or 'http://127.0.0.1:8000/health'
    response = requests.get(url)
    print(response.json())
