'''
    Average Calculation Method
'''
import logging
import json
import numpy
import time
import os, fnmatch

from task import face_rec
from lfw import lfw_acquisition


PATH = '/svc/images'


if __name__ == "__main__":
    list_files = os.listdir('{0}/'.format(PATH))
    pattern = "*.log"

    for entry in list_files:
        if fnmatch.fnmatch(entry, pattern):
            file_path = entry

    while not os.path.exists(file_path):
        time.sleep(1)

    if os.path.isfile(file_path):
        log = logging.getLogger('master')
        handler = logging.FileHandler('{0}/{1}.log'.format(PATH, uid))
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)

        url_file = '{0}/url'.format(PATH)

        with open(url_file) as read_file:
            url = read_file.read()

        md5sum_file = '{0}/md5sum'.format(PATH)

        with open(md5sum_file) as read_file:
            md5sum = read_file.read()

        log.info('Starting Master Process...')

        dataset_list = lfw_acquisition(url=url, md5sum=md5sum, path=PATH)

        log.info('Starting Creating Tasks...')
        results = []

        for data in dataset_list[:10]:
            results.append(face_rec.delay(image_path=data))

        total_tasks = len(results)
        tasks_done = []
        count = 0

        log.info('Total of Tasks Created: %s' % total_tasks)
        log.info('Getting Tasks Done...')

        while count < total_tasks:

            for query in results:
                if query.ready():
                    tasks_done.append(query.get(timeout=10))
                    count += 1

        log.info('Calculating Average Vectors...')

        average = numpy.array(tasks_done[0][1])

        for done in tasks_done[1:]:

            if done[1] is not None:
                average = (average + numpy.array(done[1])) / 2

        log.info('Result of calculation the average of values: %s' % average)
