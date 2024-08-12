from app import db, Room, app

# Define 10 room fixtures
rooms = [
    {'name': 'Conference Room A', 'capacity': 10, 'projector': True, 'sound': True},
    {'name': 'Conference Room B', 'capacity': 20, 'projector': False, 'sound': True},
    {'name': 'Meeting Room 1', 'capacity': 5, 'projector': False, 'sound': False},
    {'name': 'Meeting Room 2', 'capacity': 8, 'projector': True, 'sound': False},
    {'name': 'Board Room', 'capacity': 15, 'projector': True, 'sound': True},
    {'name': 'Training Room', 'capacity': 25, 'projector': True, 'sound': True},
    {'name': 'Lounge', 'capacity': 7, 'projector': False, 'sound': True},
    {'name': 'Executive Suite', 'capacity': 4, 'projector': True, 'sound': False},
    {'name': 'Workshop Room', 'capacity': 12, 'projector': False, 'sound': True},
    {'name': 'Interview Room', 'capacity': 3, 'projector': False, 'sound': False},
]

def add_fixtures():
    for room in rooms:
        existing_room = Room.query.filter_by(name=room['name']).first()
        if not existing_room:
            new_room = Room(**room)
            db.session.add(new_room)
    db.session.commit()
    print("10 rooms added successfully!")

if __name__ == "__main__":
    with app.app_context():
        add_fixtures()
