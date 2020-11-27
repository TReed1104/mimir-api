## Imports
from datetime import datetime
from flask import request
from flask_restful import Resource, abort
from flask_jsonpify import jsonify
from webargs import fields
from webargs.flaskparser import use_args
from shared import db
from models.timetable import Timetable
from models.booking import Booking

class BookingHandler(Resource):
    get_and_delete_args = {
        'id': fields.Integer(required=True)
    }
    post_args = {
        'timetable': fields.String(required=True),
        'name': fields.String(required=True),
        'start': fields.DateTime(required=True),
        'end': fields.DateTime(required=True),
        'colour': fields.String(required=True)
    }
    put_args = {
        'id': fields.Integer(required=True),
        'name': fields.String(),
        'colour': fields.String()
    }

    @use_args(get_and_delete_args)
    def get(self, args):
        ## Get the booking with the supplied id, thats on the chosen timetable
        booking = Booking.query.filter_by(identifier=args['id']).first()
        ## Check we found the booking
        if booking is None:
            abort(404, message="Booking not found")
        ## Return the bookings information
        response = {
            "meta": {},
            "links": {
                "self": request.url
            },
            "data": {
                "booking": booking.serialize
            }
        }
        return jsonify(response)

    @use_args(post_args)
    def post(self, args):
        ## Check if the Timetable already exists
        timetable = Timetable.query.filter_by(name=args['timetable']).first()
        if timetable is None:
            abort(404, message='Timetable not found')
        ## Check the start date and end date of the session is the same
        if args['start'].date() != args['end'].date():
            abort(422, message="Start and End date must match")
        ## Check the end time is after the start time
        if args['start'].time() >= args['end'].time():
            abort(422, message="The session must end after its start time")
        ## Strip timezone data if its present
        args['start'] = args['start'].replace(tzinfo=None)
        args['end'] = args['end'].replace(tzinfo=None)
        ## Conflict check
        isConflicting = timetable.checkBookingConflict(args['start'], args['end'])
        if isConflicting:
            abort(422, message="Booking Conflict, A sessions already exists at this time")
        ## Parse the parameters to a dictionary for SQLAlchemy
        bookingData = {}
        bookingData['name'] = args['name']
        bookingData['start'] = args['start']
        bookingData['end'] = args['end']
        bookingData['cell_colour'] = args['colour']
        ## Create the booking object
        booking = Booking(**bookingData)
        booking.timetable_id = timetable.identifier    ## Set the bookings timetable to the found supplied one
        db.session.add(booking)
        db.session.commit()
        return "", 201

    @use_args(put_args)
    def put(self, args):
        ## Check the booking exists
        booking = Booking.query.filter_by(identifier=args['id']).first()
        if booking is None:
            abort(404, message='Booking not found')
        ## Update the supplied fields
        if 'name' in args:
            booking.name = args['name']
        if 'colour' in args:
            booking.cell_colour = args['colour']
        ## Commit to database
        booking.updated_at = datetime.now()
        db.session.commit()
        return "", 202

    @use_args(get_and_delete_args)
    def delete(self, args):
        booking = Booking.query.filter_by(identifier=args['id']).first()
        if booking is None:
            abort(404, message='Booking not found')
        ## Execute the delete
        db.session.delete(booking)
        db.session.commit()
        return "", 202
