from rollcall import app
import rollcall.faces as faces
import rollcall.helper as helper
from os import path, rename, makedirs
import datetime as dt
import logging


def identify(base64photo):
    '''Identify the member from a photo
    Returns:
        member object if identified, else None
        Photo ID, None if invalid image
    '''
    photoId = faces.detect(base64photo)
    if not photoId: 
        logging.error('No face in photo')
        return None, None
    
    member = faces.recognise(photoId)
    if not member: 
        logging.info('Member not identified')
        return None, photoId
    
    logging.info(f'Member identified: {member}')
    return member, photoId


def register(member, photoId):
    '''Record the member's presence at the meeting
    Returns:
        member object if identified by memberId, else None
        photoId used to register the member, None if invalid
        an appropriate message
    '''
    #Sanity checks
    if not photoId: return None, None, 'photoId not provided'
    photo = f'{photoId}.jpg'
    srcDir = path.join(app.config['DATA'], 'faces')
    if not path.exists(path.join(srcDir, photo)): return None, None, 'Invalid photoId'

    member = helper.findMember(member)
    if not member: return None, photoId, "Member not found"
    id = member.get('id')

    #Move the new photo to the member's directory
    dstDir = path.join(srcDir, f'{int(id):06d}')
    makedirs(dstDir, exist_ok=True)
    rename(path.join(srcDir, photo), path.join(dstDir, photo))

    _record(id)

    return member, photoId, 'Member registered successfully'


def _record(memberId):
    today = dt.datetime.today()
    register = path.join(app.config['DATA'], f'{today.year}-{today.month:02}-{today.day:02}.txt') 
    with open(register, 'a') as f: 
        f.write(f'{memberId}\n')
