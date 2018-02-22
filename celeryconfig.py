worker_task_log_format = "[%(asctime)s: %(levelname)s/%(name)s] %(message)s"

# the following settings ensure that one docker container gets one celery task once with no prefetch
# http://celery.readthedocs.io/en/latest/userguide/optimizing.html
task_acks_late = True
worker_prefetch_multiplier = 1

# https://stackoverflow.com/questions/27310899/celery-is-rerunning-long-running-completed-tasks-over-and-over
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_transport_options
broker_transport_options = {'visibility_timeout': 3600*100}  # 100 hours
