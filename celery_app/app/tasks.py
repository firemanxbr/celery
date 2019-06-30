from celery import Celery, Task

from app.lfw import lfw_acquisition

# URL to connect to broker
broker_url = 'amqp://celery_user:secret@rabbitmq:5672/celery_app'

# Create Celery application
application = Celery('tasks', broker=broker_url)

URL = 'http://vis-www.cs.umass.edu/lfw/lfw.tgz'
MD5SUM = 'a17d05bd522c52d84eca14327a23d494'


class TaskError(Exception):
    """Custom exception for handling task errors"""
    pass


class AppBaseTask(Task):
    """Base Task

    The base Task class can be used to define
    shared behaviour between tasks.

    """
    abstract = True

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # TODO: log out here
        super(AppBaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # TODO: log out here
        super(AppBaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


@application.task(base=AppBaseTask, bind=True, max_retries=3, soft_time_limit=5)
def do_task(self, url, md5sum, path=None):
    """
    """
    try:
        DATASET_LIST = lfw_acquisition(url=URL, md5sum=MD5SUM, path='/celery_app/data/')
        return DATASET_LIST
        
    except Exception as se:
        self.retry(countdown=10, exc=se)
    except Exception as exc:
        raise TaskError(exc)
