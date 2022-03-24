from http import HTTPStatus
from flask import request, jsonify
from rollcall import app
import rollcall.api as api

@app.route('/')
def test():
    member = api.test()
    return jsonify(message='Welcome to Rollcall API'), HTTPStatus.OK


@app.route('/identify', methods=['POST'])
def identify():
    photo = request.get_json(force=True).get('photo')
    if photo == None: return jsonify(message='No photo provided'), HTTPStatus.BAD_REQUEST

    member, photoGuid = api.identifyMember(photo)
    if photoGuid == None: return jsonify(message='Bad photo'), HTTPStatus.BAD_REQUEST

    status = HTTPStatus.NOT_FOUND if member == None else HTTPStatus.OK
    return jsonify(photoGuid=photoGuid, member=member), status


@app.route('/register', methods=['POST'])
def register():
    json = request.get_json(force=True)
    photoGuid = json.get('photoGuid')
    if photoGuid == None: return jsonify(message='Missing photoGuid'), HTTPStatus.BAD_REQUEST
    memberId = json.get('memberId')
    if memberId == None: return jsonify(message='Missing memberId'), HTTPStatus.BAD_REQUEST

    member = api.registerMember(memberId, photoGuid)
    status = HTTPStatus.NOT_FOUND if member == None else HTTPStatus.OK
    return jsonify({ 'member': member }), status