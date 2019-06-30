"""
"""
import face_recognition
import hashlib
import requests
import numpy as np


URL = 'http://vis-www.cs.umass.edu/lfw/lfw.tgz'
MD5SUM = 'a17d05bd522c52d84eca14327a23d494'


#r = requests.get(URL)

#with open("lfw.tgz", "wb") as code:
#    code.write(r.content)

# print(hashlib.md5(open('lfw.tgz','rb').read()).hexdigest())


#photo1 = face_recognition.load_image_file("lfw/Aaron_Peirsol/Aaron_Peirsol_0001.jpg")
photo1 = face_recognition.load_image_file("lfw/Peggy_McGuinness/Peggy_McGuinness_0001.jpg")
photo_encoding1 = face_recognition.face_encodings(photo1)[0]

#photo2 = face_recognition.load_image_file("lfw/Miguel_Contreras/Miguel_Contreras_0002.jpg")
#photo_encoding2 = face_recognition.face_encodings(photo2)[0]

print(photo_encoding1)
#print(photo_encoding2)
#print(type(photo_encoding2))
#print(len(photo_encoding2))

#
# To find the euclidean distance between the two embeddings 
#
#distance = np.sum(np.square(photo_encoding1 - photo_encoding2))
#print(distance)

#
# METHOD 1 --- I need check it!
#
#vector1 = np.array(photo_encoding1)
#vector2 = np.array(photo_encoding2)

#sum_vector = (vector1 + vector2) / 2
#print(sum_vector)


#
# METHOD 2 --- This is right? I don't know!
#
#print((photo_encoding1 + photo_encoding2) / 2)

#
# METHOD 3 --- WRONG !!!
#
#print(np.mean(photo_encoding1, axis=0))