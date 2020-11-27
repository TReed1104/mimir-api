from datetime import datetime
from shared import db

class Booking(db.Model):
    __tablename__ = 'mimir_bookings'
    identifier = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    start = db.Column(db.DateTime, nullable=False, default=datetime.now)
    end = db.Column(db.DateTime, nullable=False, default=datetime.now)
    cell_colour = db.Column(db.String(255), unique=False, nullable=False)
    timetable_id = db.Column(db.Integer, db.ForeignKey('mimir_timetables.identifier'))
    timetable = db.relationship('Timetable', back_populates="bookings")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @property
    def duration(self):
        return abs(self.end - self.start).total_seconds() / 3600

    @property
    def timetable_name(self):
        if timetable is not None:
            return timetable.name
        return "Not Set"

    @property
    def serialize(self):
        return {
            'id': self.identifier,
            'booking': self.name,
            'timetable': self.timetable.name,
            'timetable_id': self.timetable_id,
            'start_time': self.start,
            'end_time': self.end,
            'duration': self.duration,
            'cell_colour': self.cell_colour
        }
