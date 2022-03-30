from http import HTTPStatus
from flask import request, jsonify
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
    json = request.get_json(force=True)
    photoId = json.get('photoId')
    if photoId == None: return jsonify(message='Missing photoId'), HTTPStatus.BAD_REQUEST
    member = json.get('memberId')
    if member == None: return jsonify(message='Missing member ID'), HTTPStatus.BAD_REQUEST

    try:
        member, photoId, message = api.register(member, photoId)
        if photoId == None:
            status = HTTPStatus.BAD_REQUEST
        else:
            status = HTTPStatus.NOT_FOUND if member == None else HTTPStatus.CREATED
    except Exception:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        message = 'Failed to register member'
    return jsonify(message=message)