from rollcall import app, members
import rollcall.faces as faces
from uuid import uuid1
from os import path, rename, makedirs
from base64 import b64decode
import numpy as np
import cv2
import logging


def test():
    global members
    return members['052450']


def identifyMember(base64photo):
    '''Identify the member from a photo
    Returns:
        member object if identified, else None
        GUID of the photo, None if invalid image
    '''
    faceGuid = faces.detectFace(base64photo)
    if faceGuid == None: 
        logging.error('No face in photo')
        return None, None
    memberId = faces.recogniseMember(faceGuid)
    if memberId == None: 
        logging.info('Member not recognised')
        return None, faceGuid
    global members
    member = members.get(memberId)
    logging.info(f'Member recognised: {member}')
    return member, faceGuid


def registerMember(memberId, photoGuid):
    '''Record the member's presence at the meeting
    Returns:
        member object if identified by memberId, else None
    '''
    #Move the new face to the member's directory
    memberId = f'{int(memberId):06d}'
    srcDir = path.join(app.config['DATA'], 'faces')
    dstDir = path.join(srcDir, memberId)
    makedirs(dstDir, exist_ok=True)
    rename(path.join(srcDir, photoGuid), path.join(dstDir, photoGuid))

    global members
    return members[memberId] if memberId in members else None 
