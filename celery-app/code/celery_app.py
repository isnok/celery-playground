import logging

logger = logging.getLogger()

from celery import Celery, shared_task
import time

# Celery Config

app = Celery()
celeryconfig = {
    'BROKER_URL': 'amqp://rabbit',
    'CELERY_RESULT_BACKEND': 'redis://redis',
}

# from kombu import Exchange, Queue
# celeryconfig['CELERY_QUEUES'] = (
    # Queue('tasks', Exchange('tasks'), routing_key='tasks',
          # queue_arguments={'x-max-priority': 10}),
# )
# celeryconfig['CELERY_ACKS_LATE'] = True
# celeryconfig['CELERYD_PREFETCH_MULTIPLIER'] = 1

app.config_from_object(celeryconfig)

@shared_task
def sleep(seconds):
    """ A helpful task for debugging asynchronous execution. """

    logger.info("Started sleep for {} seconds.".format(seconds))
    time.sleep(seconds)
    logger.info("Done sleeping for {} seconds.".format(seconds))

    return seconds
