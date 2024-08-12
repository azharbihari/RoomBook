import unittest
import json
from app import app, db, Room, Booking
from datetime import datetime, timedelta


class RoomBookingTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client and initialize the database
        self.app = app.test_client()
        self.app.testing = True
        
        # Create a new in-memory database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()
        
            # Add a sample room to the database
            room = Room(name="Conference Room", capacity=10, projector=True, sound=True)
            db.session.add(room)
            db.session.commit()


    def tearDown(self):
        # Drop all tables after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_rooms(self):
        # Test retrieving rooms without a search query
        response = self.app.get('/api/rooms')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)  # Should return one room

    def test_get_room_by_id(self):
        # Test retrieving a room by ID
        response = self.app.get('/api/rooms/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Conference Room")

    def test_room_availability(self):
        # Test checking room availability
        date_str = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.app.get(f'/api/rooms/1/availability/{date_str}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('09:00', data['available_slots'])  # Should have available slots

    def test_create_booking(self):
        # Test creating a new booking
        booking_data = {
            'roomId': 1,
            'startTime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'endTime': (datetime.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
        response = self.app.post('/api/bookings', data=json.dumps(booking_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('Booking successful!', data['message'])

    def test_booking_conflict(self):
        # Test creating a booking that conflicts with an existing one
        booking_data = {
            'roomId': 1,
            'startTime': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'endTime': (datetime.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
        # First booking should succeed
        response = self.app.post('/api/bookings', data=json.dumps(booking_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Second booking should fail due to conflict
        response = self.app.post('/api/bookings', data=json.dumps(booking_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
