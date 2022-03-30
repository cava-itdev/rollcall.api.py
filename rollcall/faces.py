import os
import cv2
import numpy as np
import logging
from uuid import uuid1
from math import sqrt
from base64 import b64decode
from rollcall import app


def detect(base64photo):
    '''Detects a face in an image
    Returns:
        Photo ID
    '''
    #Convert base64 to grayscale image
    try:
        img_raw = b64decode(base64photo)
        img_npy = np.frombuffer(img_raw, dtype=np.uint8)
        img = cv2.imdecode(img_npy, cv2.IMREAD_UNCHANGED) #??
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        logging.info('Converted photo to grayscale image')
    except:
        logging.error('Failed to convert photo')
        return None
    #Detect face(s) in image
    try:
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
        logging.info(f'{len(faces)} face(s) detected')
        if len(faces) == 0: return None
    except:
        logging.error('Failed to detect face')
        return None

    #???
    #Save face image with GUID
    # try:
    #     ok, jpg = cv2.imencode('*.jpg', gray)
    # except:
    #     logging.error('Failed to encode jpg')
    #     return None
    photoId = str(uuid1())
    path = os.path.join(app.config['DATA'], 'faces', f'{photoId}.jpg')
    try:
        face = getLargest(faces)
        cv2.imwrite(path, gray[face[1]:face[1]+face[3], face[0]:face[0]+face[2]])
        return photoId
    except:
        logging.error('Failed to write jpg')
        return None


def recognise(faceGuid):
    #TODO: Implement
    return '052450'
    

def getLargest(faces):
    '''Helper function to select the face with the largest diagonal from a list of faces'''
    if len(faces) == 0: return None
    if len(faces) == 1: return faces[0]

    sizeOf = lambda f: sqrt(f[2]**2 + f[3]**2)
    maxSize = 0
    bigFace = faces[0]
    for face in faces:
        size = sizeOf(face)
        if size > maxSize: maxSize, bigFace = size, face
    return bigFace