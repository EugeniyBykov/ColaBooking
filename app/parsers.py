from flask_restful import reqparse

createShiftParser = reqparse.RequestParser()
createShiftParser.add_argument('room_id', type=int, required=True, help="room_id cannot be blank!")
createShiftParser.add_argument('hours_from', type=str, required=True, help="hours_from cannot be blank!")
createShiftParser.add_argument('minutes_from', type=str, required=True, help="minutes_from cannot be blank!")
createShiftParser.add_argument('hours_to', type=str, required=True, help="hours_to cannot be blank!")
createShiftParser.add_argument('minutes_to', type=str, required=True, help="minutes_to cannot be blank!")