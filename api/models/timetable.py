from datetime import datetime
from shared import db

class Timetable(db.Model):
    __tablename__ = 'mimir_timetables'
    identifier = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    bookings = db.relationship('Booking', back_populates="timetable")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @property
    def get_bookings(self):
        if self.bookings is None:
            return []
        else:
            bookings = []
            for booking in self.bookings:
                bookings.append(booking.serialize)
            return bookings

    @property
    def serialize(self):
        return {
            'id': self.identifier,
            'timetable': self.name,
            'bookings': self.get_bookings
        }

    ## Our function for checking if a new booking overlaps or conflicts with existing bookings attached to this timetable
    def checkBookingConflict(self, newBookingStart, newBookingEnd):
        ## Iterate through each booking attached to this timetable
        for booking in self.bookings:
            ## Check if the booking conflicts with the new booking
            ## Using De Morgan's Laws of boolean algebra we can derive:     (start1 <= end2) && (end1 >= start2)
            ## or to include dates being out of order:                      max(start1, start2) < min(end1, end2)
            ## See: https://stackoverflow.com/a/325964
            if max(booking.start, newBookingStart) < min(booking.end, newBookingEnd):
                return True ## Conflict found
        return False ## No conflict found
