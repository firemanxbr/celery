from celery.result import AsyncResult
from task import app

import sys



if __name__ == "__main__":
    task_id = sys.argv[1]
    res = AsyncResult(task_id, app=app)
    res.get()
