## Imports
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from models import timetable, booking
from shared import db
from resources import list_timetables, list_bookings
from resources import handler_timetables, handler_bookings

## Create our Flask app and connect it to our database
app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('configs/main.cfg')
CORS(app)
db.init_app(app)
with app.app_context():
    db.create_all()

## Register the resources and the endpoints to access them
api.add_resource(list_timetables.TimetableList, '/timetables')
api.add_resource(list_bookings.BookingList, '/bookings')
api.add_resource(handler_timetables.TimetableHandler, '/timetable_handler')
api.add_resource(handler_bookings.BookingHandler, '/booking_handler')

## Application entry point
if __name__ == '__main__':
    ## Initialise the application, 0.0.0.0 means to use our machine ip and enable debugging if needed
    app.run(host='0.0.0.0', port='5000')
