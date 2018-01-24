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


# celeryconfig['task_routes'] = { # Cannot mix new setting names with old setting names...
celeryconfig['CELERY_ROUTES'] = {
    'celery_app.normal_task': {'queue': 'celery'},
    'celery_app.prio_task': {'queue': 'priority'},

    'core.tasks.normal_task': {'queue': 'celery'},
    'core.tasks.prio_task': {'queue': 'priority'},

    'normal_task': {'queue': 'celery'},
    'prio_task': {'queue': 'priority'},

    '__main__.normal_task': {'queue': 'celery'},
    '__main__.prio_task': {'queue': 'priority'},
}

# from kombu import Exchange, Queue
# celeryconfig['CELERY_QUEUES'] = (
    # Queue('celery', Exchange('celery'), routing_key='celery',
          # # queue_arguments={'x-max-priority': 10}
    # ),
    # Queue('prio', Exchange('prio'), routing_key='prio',
          # # queue_arguments={'x-max-priority': 10}
    # ),
# )
# celeryconfig['CELERY_ACKS_LATE'] = True
# celeryconfig['CELERYD_PREFETCH_MULTIPLIER'] = 1

app.config_from_object(celeryconfig)

from itertools import cycle
import string

def id_generator():
    letters = cycle(string.ascii_uppercase)
    numbers = string.digits

    while True:
        first = next(letters)
        for second in numbers:
            yield '{}_{}'.format(first, second)

id_gen = id_generator()

def raw_task(seconds, identifier):
    """ A helpful task for debugging asynchronous execution. """

    logger.info("Started {} for {} seconds.".format(identifier, seconds))
    time.sleep(seconds)
    logger.info("Done with {} after {} seconds.".format(identifier, seconds))

    return identifier, seconds


@shared_task
def normal_task(*args, **kwd):
    return 'normal', raw_task(*args, **kwd)

@shared_task
def prio_task(*args, **kwd):
    return 'prio', raw_task(*args, **kwd)


def create_tasks(count, seconds=23, prio=False):
    task = {True: prio_task, False: normal_task}[prio]
    tasks = []

    for i in range(count):
        tasks.append(task.delay(seconds, identifier=next(id_gen)))

    return tasks


# celery does not like this... (tasks from __main__)
# if __name__ == '__main__':
    # logger.info('Starting 10 normal tasks...')
    # create_tasks(10)

    # logger.info('Starting 10 priority tasks...')
    # create_tasks(10, prio=True)
