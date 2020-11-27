## Imports
from datetime import datetime
from flask import request
from flask_restful import Resource
from flask_jsonpify import jsonify
from shared import db
from models.timetable import Timetable

## Resource for getting a list of the timetables in the system
class TimetableList(Resource):
    ## The GET method endpoint
    def get(self):
        ## Get all the timetables registered with Mimir
        timetables = Timetable.query.all()
        timetableResponseArray = []
        if timetables is not None:
            timetableResponseArray = [timetable.serialize for timetable in timetables]
        ## Generate our JSON response
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "timetables": timetableResponseArray
            }
        }
        return jsonify(response)
