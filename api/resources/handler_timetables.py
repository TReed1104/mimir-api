from datetime import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db
from models.timetable import Timetable

class TimetableHandler(Resource):
    get_and_delete_args = {
        'id': fields.Integer(required=True)
    }
    post_args = {
        'name': fields.String(required=True)
    }
    put_args = {
        'id': fields.Integer(required=True),
        'new_name': fields.String(required=True)
    }

    @use_args(get_and_delete_args)
    def get(self, args):
        ## Try and find the timetable
        timetable = Timetable.query.filter_by(identifier=args['id']).first()
        ## Check we found the timetable
        if timetable is None:
            abort(404, message="Timetable not found")
        ## Return out result
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "timetable": timetable.serialize
            }
        }
        return jsonify(response)

    @use_args(post_args)
    def post(self, args):
        ## Check if the Timetable already exists
        doesTimetableExist = Timetable.query.filter_by(name=args['name']).first()
        if doesTimetableExist is not None:
            abort(422, message='The supplied Timetable Name already exists')
        ## Map the data to a dictionary
        timetableData = {}
        timetableData['name'] = args['name']
        ## Create the timetable
        timetable = Timetable(**timetableData)
        db.session.add(timetable)
        db.session.commit()
        return "", 201

    @use_args(put_args)
    def put(self, args):
        ## Check the timetable we are renaming exists in the system
        doesTimetableExist = Timetable.query.filter_by(identifier=args['id']).first()
        if doesTimetableExist is None:
            abort(404, message="Timetable not found")
        ## Check the new name for the timetable doesn't already exist
        doesNewTimetableExist = Timetable.query.filter_by(name=args['new_name']).first()
        if doesNewTimetableExist is not None:
            abort(422, message='The new timetable name already exists')
        ## Map the request data to a dictionary
        timetableData = {}
        timetableData['name'] = args['new_name']
        ## Update the timetable using the dictionary
        timetable = Timetable.query.filter_by(identifier=doesTimetableExist.identifier)
        timetable.update(timetableData)
        timetable.first().updated_at = datetime.now()
        db.session.commit()
        ## Return that the resource has been updated
        return "", 202

    @use_args(get_and_delete_args)
    def delete(self, args):
        ## Check the timetable we are renaming exists in the system
        timetable = Timetable.query.filter_by(identifier=args['id']).first()
        if timetable is None:
            abort(404, message="Timetable not found")
        ## Execute the delete
        db.session.delete(timetable)
        db.session.commit()
        return "", 202
