from flask import request, jsonify
from flask_restful import Resource, abort
from app import app, db, api
from db.models import User, MeetingRoom, Company, BookingShift
from datetime import datetime, time, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from parsers import createShiftParser
import json, uuid, jwt

class Auth(Resource):
    def post(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
          return {'message' : 'empty auth credentials'}, 401

        user = User.query.filter_by(name=auth.username).first()
        if not user:
            return {'message' : 'User with current name not found!'}, 401

        if check_password_hash(user.psw, auth.password):
            token = jwt.encode({'public_id': user.id, 'exp' : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({'token' : token})

        return {'message' : 'invalid password'}, 401

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = None

            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token:
                return {"message" :"Token is missing!"}, 401

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = User.query.filter_by(id=data['public_id']).first()
            except:
                return {"message" :"Token is invalid!"}, 401

            return f(current_user, *args, **kwargs)

        return decorator

class getAllShifts(Resource):
    @Auth.token_required
    def get(current_user, self):
        meetingRooms = MeetingRoom.query.all()
        result = {}
        for room in meetingRooms :
            bookingShift = BookingShift.query.filter_by(meeting_room_id = room.id).all()
            reserved = []
            for shift in bookingShift :
                reserved.append(
                    {"shift_id" : shift.id, "from" : shift.time_from, "to" : shift.time_to }
                )
            result[room.id] = {
                "roomName" : room.name,
                "roomId" : room.id,
                "reserved" : reserved
            }

        return jsonify(result)

class createShift(Resource):
    FROM_HOURS = 10
    TO_HOURS = 20

    @Auth.token_required
    def post(current_user, self):
        args = createShiftParser.parse_args(strict=True)
        if not self.validateTime(args['hours_from'], args['hours_to']):
            return {"reserved": False, "message" : "Rooms avaliable from {}:00 to {}:00".format(self.FROM_HOURS, self.TO_HOURS)}
        selectedRoom = MeetingRoom.query.get(args['room_id'])
        if not selectedRoom or selectedRoom.company_id != current_user.company_id :
            return {"reserved": False, "message" :"meeting room belong to other company"}

        bookingShifts = BookingShift.query.filter_by(meeting_room_id = args['room_id']).all()
        reserved = False
        today = date.today()
        try:
            timeFrom = datetime.combine(today,time(int(args["hours_from"]), int(args["minutes_from"])))
            timeTo = datetime.combine(today,time(int(args["hours_to"]), int(args["minutes_to"])))
        except:
            return {"reserved": False, "message" : "Wrong time format"}

        if timeTo < timeFrom:
            return {"reserved": False, "message" :"Wrong time period"}

        for shift in bookingShifts :
            if (
                (timeFrom >= shift.time_from and timeFrom <= shift.time_to)
                or (timeTo >= shift.time_from and timeTo <= shift.time_to)
            ):
                reserved = True
                break

        if reserved:
            return {"reserved": False, "message" : "Current time is reserved!"}

        try:
            bookingShift = BookingShift(
                user_id=current_user.id,
                meeting_room_id=selectedRoom.id,
                time_from=timeFrom,
                time_to=timeTo
            )
            db.session.add(bookingShift)
        except:
             db.session.rollback()
             return {"reserved": False, "message" : "Error to reserve meeting room, please try later!"}
        else:
             db.session.commit()

        return jsonify({"reserved": True, "message" : "You successfully reserved room"})

    def validateTime(self, hours_from, hours_to):
        try:
            if int(hours_from) < self.FROM_HOURS or int(hours_to) > self.TO_HOURS:
                return False
        except:
            return False

        return True

class DeleteShiftById(Resource):
    @Auth.token_required
    def delete(current_user, self, shift_id):
        self.abortIfShiftDoesntExist(shift_id)
        try:
            BookingShift.query.filter_by(id=shift_id).delete()
        except:
            db.session.rollback()
        else:
            db.session.commit()

        return {"cancel_reservation" : True, "message" : "Reservation has been canceled"}

    def abortIfShiftDoesntExist(self, shift_id):
        shift = BookingShift.query.get(shift_id)
        if not shift:
            abort(404, message="Shift {} doesn't exist".format(shift_id))


api.add_resource(Auth, '/api/auth')
api.add_resource(getAllShifts, '/api/shifts/all')
api.add_resource(createShift, '/api/shifts/add')
api.add_resource(DeleteShiftById, '/api/shifts/delete/<shift_id>')