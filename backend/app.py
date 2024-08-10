from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_cors import CORS
import pytz
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./bookings.db' 
db = SQLAlchemy(app)
CORS(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer)
    projector = db.Column(db.Boolean, default=False)
    sound = db.Column(db.Boolean, default=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    code = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

with app.app_context():
    db.create_all()




@app.route('/api/rooms')
def get_rooms():
    search_query = request.args.get('q', '')
    if search_query:
        rooms = Room.query.filter(Room.name.ilike(f'%{search_query}%')).all()
    else:
        rooms = Room.query.all()

    # Get the current date and time for availability check in Asia/Kolkata timezone
    local_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(local_tz).date()

    room_list = []
    for room in rooms:
        # Get bookings for the room on the current date
        bookings = Booking.query.filter_by(room_id=room.id).filter(
            Booking.start_time >= datetime.combine(now, datetime.min.time()),
            Booking.start_time < datetime.combine(now, datetime.max.time())
        ).all()

        available_slots = []
        for hour in range(9, 18):
            start_time = datetime.combine(now, datetime.min.time()) + timedelta(hours=hour)
            end_time = start_time + timedelta(hours=1)

            # Check if any bookings overlap with this time slot
            is_booked = any(
                (booking.start_time < end_time and booking.end_time > start_time)
                for booking in bookings
            )

            if not is_booked:
                available_slots.append(start_time.strftime('%H:%M'))

        room_list.append({
            'id': room.id,
            'name': room.name,
            'capacity': room.capacity,
            'projector': room.projector,
            'sound': room.sound,
            'available_slots': available_slots  # Add availability to the response
        })

    return jsonify(room_list)

@app.route('/api/rooms/<int:room_id>')
def get_room(room_id):
    room = Room.query.get_or_404(room_id)
    return jsonify({'id': room.id, 'name': room.name, 'capacity': room.capacity, 
                  'projector': room.projector, 'sound': room.sound})


@app.route('/api/rooms/<int:room_id>/availability/<date_str>')
def get_availability(room_id, date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    room = Room.query.get_or_404(room_id)
    bookings = Booking.query.filter_by(room_id=room_id).filter(
        Booking.start_time.between(datetime.combine(date, datetime.min.time()), datetime.combine(date, datetime.max.time()))
    ).all()



    available_slots = []
    for hour in range(9, 18):
        start_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour)
        end_time = start_time + timedelta(hours=1)

        # Check if the time slot is free (i.e., no overlapping bookings)
        is_booked = any(
            (booking.start_time < end_time and booking.end_time > start_time)
            for booking in bookings
        )

        if not is_booked:
            available_slots.append(start_time.strftime('%H:%M'))
        

    return jsonify({'available_slots': available_slots})

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()

    # Parse the incoming UTC datetime strings to datetime objects
    utc_start_time = datetime.strptime(data['startTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_end_time = datetime.strptime(data['endTime'], '%Y-%m-%dT%H:%M:%S.%fZ')

    # Convert UTC times to local time (Asia/Kolkata)
    local_tz = pytz.timezone('Asia/Kolkata')
    local_start_time = utc_start_time.replace(tzinfo=pytz.utc).astimezone(local_tz).replace(tzinfo=None)
    local_end_time = utc_end_time.replace(tzinfo=pytz.utc).astimezone(local_tz).replace(tzinfo=None)

    # Create a new booking with the local times
    unique_code = str(uuid.uuid4())  # Generate a unique code for the booking
    new_booking = Booking(
        room_id=data['roomId'], 
        start_time=local_start_time, 
        end_time=local_end_time,
        code=unique_code
    )
    
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({
        'message': f'Booking successful! Access your booked room with this code: {unique_code}',
        'code': unique_code
    }), 201

if __name__ == '__main__':
    app.run(debug=True)