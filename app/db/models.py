from app import db

class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class MeetingRoom(db.Model):
    __tablename__ = "meeting_rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    company = db.relationship("Company", backref="meeting_rooms")

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    psw = db.Column(db.String, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    company = db.relationship("Company", backref="users")

class BookingShift(db.Model):
    __tablename__ = "book_shifts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    meeting_room_id = db.Column(db.Integer, db.ForeignKey('meeting_rooms.id'))
    time_from = db.Column(db.DateTime, nullable=False)
    time_to = db.Column(db.DateTime, nullable=False)

    meeting_room = db.relationship("MeetingRoom", backref="book_shifts")
    user = db.relationship("User", backref="book_shifts")