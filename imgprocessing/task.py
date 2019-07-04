'''
    Celery Tasks that will be run by workers containers
'''
import json
import logging
import time

from celery import Celery

import face_recognition


app = Celery('task',
             broker='amqp://imgprocessing:imgprocessing@rabbitmq:5672/imgprocessing',
             backend='amqp://imgprocessing:imgprocessing@rabbitmq:5672/imgprocessing')

#URL = 'http://vis-www.cs.umass.edu/lfw/lfw.tgz'
#MD5SUM = 'a17d05bd522c52d84eca14327a23d494'
PATH = '/svc/images'


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

    url_file = '{0}/url'.format(PATH)

    with open(url_file, "w") as write_file:
        write_file.write(url)  

    md5sum_file = '{0}/md5sum'.format(PATH)

    with open(md5sum_file, "w") as write_file:
        write_file.write(md5sum)

    return uid


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
