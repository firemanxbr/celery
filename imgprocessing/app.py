import os
import uuid

from flask import Flask
from flask import request
from flask import Response
import json
import numpy

import task


app = Flask(__name__)
PATH = '/svc/images'


@app.route('/run')
def run():
    '''
    Function to receive the request to start the process
    '''
    url = request.args.get('url')
    md5sum = request.args.get('md5sum')

    assert url is not None
    assert md5sum is not None

    uid = str(uuid.uuid4())
    task.master.delay(url, uid, md5sum)

    return 'Process ID: {0}'.format(uid)


@app.route('/status/<uid>')
def status(uid):
    '''
    Function to show the results
    '''
    log_file = '{0}/{1}.log'.format(PATH, uid)

    if not os.path.isfile(log_file):
        return Response('Log still not available.', mimetype='text/txt')

    with open(log_file) as read_file:
        content = read_file.read()

    return Response(content.encode(), mimetype='text/txt')
