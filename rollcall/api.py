from rollcall import app, members
import rollcall.faces as faces
from os import path, rename, makedirs
from genericpath import exists
from uuid import uuid1
from base64 import b64decode
import logging


def identify(base64photo):
    '''Identify the member from a photo
    Returns:
        member object if identified, else None
        Photo ID, None if invalid image
    '''
    photoId = faces.detect(base64photo)
    if photoId == None: 
        logging.error('No face in photo')
        return None, None
    
    memberId = faces.recognise(photoId)
    if memberId == None: 
        logging.info('Member not identified')
        return None, photoId
    
    global members
    member = members.get(memberId)
    logging.info(f'Member identified: {member}')
    return None, photoId


def register(memberId, photoId):
    '''Record the member's presence at the meeting
    Returns:
        member object if identified by memberId, else None
        photoId used to register the member
    '''
    #Sanity checks
    if not photoId: return None, None
    srcDir = path.join(app.config['DATA'], 'faces')
    if not exists(path.join(srcDir, f'{photoId}.jpg')): return None, None

    #Move the new photo to the member's directory
    memberId = f'{int(memberId):06d}'
    dstDir = path.join(srcDir, memberId)
    makedirs(dstDir, exist_ok=True)
    rename(path.join(srcDir, photoId), path.join(dstDir, photoId))

    global members
    member = members.get(memberId)
    if member == None: return None, photoId

    record(member)
    return member, photoId

def record(member):
    pass