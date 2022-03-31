from http import HTTPStatus
from flask import request, jsonify
from numpy import object_
from rollcall import app
import rollcall.api as api

@app.route('/',    methods=['GET'])
@app.route('/api', methods=['GET'])
def welcome():
    return jsonify(message='Welcome to the Rollcall API'), HTTPStatus.OK


@app.route('/api/identify', methods=['POST'])
def identify():
    photo = request.get_json(force=True).get('photo')
    if photo == None:
        return jsonify(message='No photo'), HTTPStatus.BAD_REQUEST

    member, photoId = api.identify(photo)
    if photoId == None:
        return jsonify(message='Bad photo'), HTTPStatus.BAD_REQUEST

    status = HTTPStatus.NOT_FOUND if member == None else HTTPStatus.OK
    return jsonify(photoId=photoId, member=member), status


@app.route('/api/register', methods=['POST'])
def register():
    req_data = request.get_json(force=True)
    photoId = req_data.get('photoId')
    if not photoId: return jsonify(message='photoId not provided'), HTTPStatus.BAD_REQUEST
    member = req_data.get('member') # member is a dictionary
    if not member: return jsonify(message='member not provided'), HTTPStatus.BAD_REQUEST
    if not member.get('id') and not member.get('altId'): 
        return jsonify(message='member ID not provided'), HTTPStatus.BAD_REQUEST

    try:
        member, photoId, message = api.register(member, photoId)
        if photoId: status = HTTPStatus.CREATED if member else HTTPStatus.NOT_FOUND
        else: status = HTTPStatus.BAD_REQUEST
    except Exception:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        message = 'Failed to register member'
    return jsonify(member=member, photoId=photoId, message=message), status