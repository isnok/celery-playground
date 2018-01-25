# Celery Docker Appliance

This repository contains a "small" appliance built with `docker-compose` to set up a `celery` cluster.


## Installation

Get `docker` and `docker-compose`, then it should be as easy as runnning:

```
    docker-compose up
```

from the repo root.
This should fetch, build and start all containers.

Once they are running you can attach the commander container to issue commands like so:
```
    docker exec -it celeryplayground_commander_1 /bin/bash
```
The name of the container may differ (depending on your checkout folder name).
You can check that with `docker ps`.

Once inside the commader container, you can start tasks by executing `/code/launcher.py`.

## How to use it?

It is created for playing around with several features of `celery`.
The cluster is set up to communicate via `rabbitmq` and uses `redis` as the result backend.
Modify it, test your stuff, play around.
There is a minimal python app included, that has two tasks:
 - `normal_task`: sleeps for some time, at normal priority
 - `prio_task`: sleeps for some time, at high priority

The priorities are implemented through different queues, which is the recommended way.
Normal tasks use celery's default queue, named `celery`.
Priority tasks use a separate queue, named `priority`.
The tasks are configured to their queues via the config option `CELERY_ROUTES`.

## Celery commandline tools

If any celery component (a worker or a commandline task) is executed, it requires a module name that contains a celery app.
There it will find the celery configuration (the tasks, broker, result backend, etc.) to reach the cluster.
All celery commands use the commandline option `-A <mod_name>` for that purpose.
If `-A` is not specified, celery will try to read that module name from the environment variable `CELERY_APP` before giving up.
`CELERY_APP` is set in all containers, so it can be omitted.

*Note that* `celery_app.py` is not installed globally, so you have to be in the folder `/code` for any commands to work.


## Some useful commands

In the commander container:
```
    celery status
    celery inspect active
    celery inspect stats
```

In the `rabbitmq` container:
```
rabbitmqctl list_queues name messages messages_ready messages_unacknowledged
```

From another container it should be doable, after syncing `/var/lib/rabbitmq/.erlang.cookie` by issuing this:

```
rabbitmqctl -n rabbit@rabbit list_queues name messages messages_ready messages_unacknowledged
```


## Monitoring with flower

`flower` is the official recommended monitoring frontend.
It is set up in a compose config named `monitor`.
There it is specified, that port 5555 (default of flower interface) is mapped to your local host (127.0.0.1).
So, when the container is running, you should be able to reach it at [localhost:5555](http://127.0.0.1:5555) conveniently.

## More on configuration

Celery supports two ways of configuration.
The old style uses all uppercase options, while the new way uses lowercase settings.
Both variants cannot be mixed in one configuration.

An example:

- Old style: `CELERY_ROUTES = {'some_module.task_name': {'queue': 'queue_name'}}`
- New style: `task_routes = {'some_module.task_name': {'queue': 'queue_name'}}`
