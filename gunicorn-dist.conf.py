# -*- coding: utf-8 -*-
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
pidfile = '/tmp/example.pid'
logfile = '/tmp/example.log'
loglevel = 'warning'
django_settings = ''
