# Celery Docker Appliance

This repository contains a "small" appliance built with `docker-compose` to set up a `celery` cluster.


## Installation

Get `docker` and `docker-compose`, then it should be as easy as runnning:

```
    docker-compose up
```

from the repo root.


## How to use it?

It is created for playing around with several features of `celery`.
The cluster is set up to communicate via `rabbitmq` and uses `redis` as the result backend.
Modify it, test your stuff, play around.
There is a minimal python app included, that has exactly one task: `sleep`.
Use it to debug whatever you want or exend it to your needs.


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
