import time
import numpy
import face_recognition
import logging
import json
import subprocess

from celery import Celery

from lfw import lfw_acquisition


app = Celery('task',
             broker='amqp://imgprocessing:imgprocessing@rabbitmq:5672/imgprocessing',
             backend='amqp://imgprocessing:imgprocessing@rabbitmq:5672/imgprocessing')

URL = 'http://vis-www.cs.umass.edu/lfw/lfw.tgz'
MD5SUM = 'a17d05bd522c52d84eca14327a23d494'
PATH = '/svc/images'
LOCAL_TIME = time.localtime()


@app.task
def master(url, uid, md5sum=None):
    '''
    Main function to generate tasks to workers,
    getting the return of these tasks and calculate the
    average of all photos.
    '''
    log = logging.getLogger('master')
    handler = logging.FileHandler('{0}/{1}.log'.format(PATH, uid))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    log.info('Starting Producer Process...')
    
    if url and md5sum:
        DATASET_LIST = lfw_acquisition(url=url, md5sum=md5sum, path=PATH)

    else:
        DATASET_LIST = lfw_acquisition(url=URL, md5sum=MD5SUM, path=PATH)

    log.info('Starting Creating Tasks...')

    results = []

    # LIMITED in 10 Images !!!
    for data in DATASET_LIST[:10]:
        results.append(face_rec.delay(image_path=data))

    total_tasks = len(results)
    log.info('Total of tasks added: {0}'.format(total_tasks))

    tasks_done = []
    count = 0
    
    log.info('Getting Tasks Done...')

    print('RESULTS: ', results)

    while count < total_tasks:

        for query in results:
            if query.ready():
                print('QUERY: ', query)
                command = subprocess.run(['python3', 'task_result.py', '%s' % query], stdout=subprocess.PIPE)
                content = command.stdout.decode('utf-8')
                print('CONTENT: ', content)
                print('TYPE: ', type(content))
                tasks_done.append(list(content))
                count += 1

    print('TASKS DONE: ', tasks_done)

    log.info('Total of tasks finished: {0}'.format(count))
    log.info('Calculating Average Vectors...')

    average = numpy.array(tasks_done[0][1])

    for done in tasks_done[1:]:
        average = (average + numpy.array(done[1])) / 2

    log.info('Result of calculation the average of photos: {0}'.format(average))


@app.task
def face_rec(image_path):
    '''
    Function to get the vectors of a photo
    '''
    photo = face_recognition.load_image_file(image_path)

    try:
        photo_encoding = list(face_recognition.face_encodings(photo)[0])
        return image_path, photo_encoding

    except IndexError:
        return image_path, None
