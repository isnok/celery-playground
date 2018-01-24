#!/usr/bin/env python

import sys
import celery_app

if __name__ == '__main__':

    if len(sys.argv) > 1:
        prio = True
    else:
        prio = False

    celery_app.create_tasks(10, prio=prio)
