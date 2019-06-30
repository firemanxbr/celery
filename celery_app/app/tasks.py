from celery import Celery, Task

from app.lfw import lfw_acquisition


URL = 'http://vis-www.cs.umass.edu/lfw/lfw.tgz'
MD5SUM = 'a17d05bd522c52d84eca14327a23d494'
BROKER_URL = 'amqp://celery_user:secret@rabbitmq:5672/celery_app'

app = Celery('veriff', broker=BROKER_URL)
#app.autodiscover_tasks()


#@app.task(bind=True, max_retries=3, soft_time_limit=5)
#def do_task(url, md5sum, path=None):
#    """
#    """
#    DATASET_LIST = lfw_acquisition(url=url, md5sum=md5sum, path=path)
#    
#    return DATASET_LIST


@app.task
def add(x, y):
    return x + y


#if __name__ == "__main__":
#    add.delay(100, 100)
