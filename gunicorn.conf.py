import multiprocessing


bind = "0.0.0.0:8000"
timeout = 300
workers = multiprocessing.cpu_count() * 2 + 1
reload = True
loglevel = 'info'
