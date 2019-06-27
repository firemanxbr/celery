import random
import numpy


def face_detection():
    return numpy.array([1, 2, 3])


def get_media(a, b):
    return (a + b) / 2


media = face_detection()
print('image array: %s' % media)

for i in range(10):
    image_array = face_detection()
    print('image array: %s' % image_array)
    media = get_media(media, image_array)
    print('media: %s' % media)