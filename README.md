# Room Booking App

This is a simple room booking application built with Flask (backend) and Next.js (frontend). It allows users to view available rooms, their amenities, and make bookings.

## Features

- **View Available Rooms:** Users can see a list of rooms with their names, capacities, and available amenities (projector, sound system).
- **Search Rooms:**  Filter rooms by name to easily find the one you're looking for.
- **Check Availability:** See the available time slots for each room on a given date.
- **Make Bookings:** Book a room for a specific time slot. Bookings are assigned a unique code for access.

## Screenshots

Here's a quick look at the app:

**Available Rooms View:**

![Available Rooms](screenshots/1.png)

**Room Availability View:**

![Room Availability](screenshots/2.png)

**Booking Process:**

![Booking Selection](screenshots/3.png)

![Booking Confirmation](screenshots/4.png)

## Technologies Used

**Backend:**

- **Flask:** Python web framework for creating the API.
- **Flask-SQLAlchemy:** ORM for interacting with the SQLite database.
- **Flask-CORS:** Enables Cross-Origin Resource Sharing for communication with the frontend.
- **pytz:**  Handles timezone conversions (important for booking accuracy).
- **UUID:** Used for generating unique booking codes.

**Frontend:**

- **Next.js:** React framework for building the user interface.
- **(Add any other frontend libraries you are using here, e.g., for styling, date/time pickers)** 

## Installation

**1. Backend Setup:**

   - **Navigate to the backend directory:**
     ```bash
     cd backend
     ```
   - **Create a virtual environment (recommended):**
     ```bash
     python3 -m venv env 
     source env/bin/activate
     ```
   - **Install dependencies:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Run the Flask app:**
     ```bash
     flask run 
     ``` 
     (This will usually start the server at `http://127.0.0.1:5000/`)

**2. Frontend Setup:**

   - **Navigate to the frontend directory:**
     ```bash
     cd frontend 
     ```
   - **Install frontend dependencies:**
     ```bash
     npm install  
     ```
   - **Start the development server:**
     ```bash
     npm run dev
     ```
     (Follow the instructions in your terminal to open the app in your browser)

## API Endpoints

**Rooms:**

- **GET /api/rooms**
   - Get a list of all rooms, including their availability for the current day in the Asia/Kolkata timezone.
   - Optional query parameter: `q` (search query for room name).
- **GET /api/rooms/:id**
    - Get details of a specific room by its ID. 
- **GET /api/rooms/:id/availability/:date**
    - Get available time slots for a room on a specific date (date format: YYYY-MM-DD). 

**Bookings:**

- **POST /api/bookings**
    - Create a new booking. Returns a success message and the unique booking code.
    - Request body (JSON):
      ```json
      {
        "roomId": 1, 
        "startTime": "2024-01-15T10:00:00.000Z", 
        "endTime": "2024-01-15T11:00:00.000Z" 
      }
      ```
      **Important:** The `startTime` and `endTime` should be in UTC as indicated by the `Z` at the end.

## Database

This app uses an SQLite database (`bookings.db` in the backend directory) to store room and booking information. The database is created automatically when the Flask app runs for the first time. 

## Future Improvements

- **User Authentication:** Add user accounts so people can manage their bookings.
- **Calendar Integration:** Allow users to view bookings in their personal calendars.
- **Real-time Updates:** Implement WebSockets or a similar technology to update availability in real-time as bookings are made.
- **More Advanced Search/Filtering:**  Allow users to filter by room capacity, amenities, and other criteria. 
- **Booking Cancellation:**  Allow users to cancel their bookings.
- **Frontend Enhancements:** Improve the user interface with a calendar view for bookings, better search/filtering options, and a more visually appealing design.

## Contributing

Feel free to contribute to this project! Open issues for bugs or feature requests, or submit pull requests with your improvements.

## Contact

- Azhar Bihari 
- azharbihari@outlook.com