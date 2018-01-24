#!/usr/bin/env python

import sys
import celery_app

if __name__ == '__main__':

    num_tasks = 10 # fixed
    seconds = 23
    prio = False

    if len(sys.argv) == 2:
        """ An int as argument changes exec time, a non-int makes the tasks prio. """
        try:
            seconds = int(sys.argv[1])
        except:
            prio = True

    elif len(sys.argv) == 3:

        seconds = int(sys.argv[1])
        prio = True

    celery_app.create_tasks(num_tasks, seconds=seconds, prio=prio)
