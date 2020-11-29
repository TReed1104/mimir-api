## Imports
from datetime import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db
from models.booking import Booking
from models.timetable import Timetable

## Resource for listing the bookings for a current room
class BookingList(Resource):
    ## List the valid parameters
    request_args = {
        'timetable': fields.String(required=True)
    }

    ## The GET method endpoint
    @use_args(request_args)
    def get(self, args):
        ## Check the timetable exists
        timetable = Timetable.query.filter_by(name=args['timetable']).first()
        if timetable is None:
            abort(404, message="Timetable not found")
        ## Get the bookings
        bookings = Booking.query.filter_by(timetable_id=timetable.identifier).all()
        bookingsResponseArray = []
        if bookings is not None:
            bookingsResponseArray = [booking.serialize for booking in bookings]
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "bookings": bookingsResponseArray
            }
        }
        return jsonify(response)
