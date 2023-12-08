from app.extensions import create_celery
from app import create_app

app = create_app('development')
celery = make_celery(app)

@celery.task
def perform_async_test(test_id: int):
    # Logic to perform test
    return results
