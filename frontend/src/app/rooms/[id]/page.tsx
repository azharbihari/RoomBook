"use client"
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const bookingTimeSlots = []; 
for (let hour = 9; hour <= 17; hour++) { 
  bookingTimeSlots.push(`${hour.toString().padStart(2, '0')}:00`);
}

export default function RoomDetails({
  params: { id },
}: {
  params: { id: string }
}) {
  const router = useRouter();

  const [room, setRoom] = useState(null);
  const [selectedDate, setSelectedDate] = useState(
    new Date().toISOString().slice(0, 10)
  );
  const [selectedTimeSlot, setSelectedTimeSlot] = useState(''); 
  const [availableSlots, setAvailableSlots] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [bookingCode, setBookingCode] = useState('');  // State for booking code

  useEffect(() => {
    const fetchRoom = async () => {
      if (!id) return;
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/rooms/${id}`);
        setRoom(response.data);
        console.log(response.data)
      } catch (error) {
        console.error('Error fetching room details:', error);
      }
    };
    fetchRoom();
  }, [id]);

  const fetchAvailability = async () => {
    if (!id) return;
    try {
      setIsLoading(true); 
      const response = await axios.get(
        `http://127.0.0.1:5000/api/rooms/${id}/availability/${selectedDate}`
      );
      setAvailableSlots(response.data.available_slots);
    } catch (error) {
      console.error('Error fetching availability:', error);
    } finally {
      setIsLoading(false); 
    }
  };

  useEffect(() => {
    fetchAvailability();
  }, [id, selectedDate]);

  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
  };

  const handleTimeSlotSelect = (slot) => {
    setSelectedTimeSlot(slot);
  };

  const handleBookingSubmit = async (event) => {
    event.preventDefault(); 

    if (!selectedTimeSlot) {
      alert('Please select a time slot!');
      return; 
    }

    try {
      const [startHour, startMinute] = selectedTimeSlot.split(':').map(Number);
      const endTime = new Date(new Date(selectedDate).setHours(startHour + 1, startMinute));

      const response = await axios.post('http://127.0.0.1:5000/api/bookings', {
        roomId: room.id,
        startTime: new Date(new Date(selectedDate).setHours(startHour, startMinute)).toISOString(),
        endTime: endTime.toISOString(),
      });

      console.log('Booking successful:', response.data); 
      setBookingCode(response.data.code);  // Save the booking code
      setSelectedTimeSlot(''); 
      fetchAvailability(); 

    } catch (error) {
      console.error('Error creating booking:', error);
    }
  };

  if (!room) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto p-4 max-w-screen-lg">
      <h1 className="text-3xl font-bold mb-4">{room.name}</h1>

      <div className="mb-4">
        <label htmlFor="booking-date" className="block mb-2">
          Select Date:
        </label>
        <input
          type="date"
          id="booking-date"
          value={selectedDate}
          onChange={handleDateChange}
          className="border border-gray-400 p-2 rounded text-black"
        />
      </div>

      {isLoading && <p>Loading availability...</p>} 

      {!isLoading && (
        <div>
          <h2 className="text-2xl font-semibold mb-2">
            Available Time Slots:
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
            {bookingTimeSlots.map((slot) => (
              <button
                key={slot}
                onClick={() => handleTimeSlotSelect(slot)}
                disabled={!availableSlots.some(
                  (s) => s === slot 
                )}
                className={`p-2 rounded border ${
                  selectedTimeSlot === slot 
                    ? 'border-green-500'
                    : availableSlots.some((s) => s === slot)
                    ? 'border-blue-500 hover:bg-blue-100'
                    : 'border-red-500 cursor-not-allowed'
                }`}
              >
                {slot}
              </button>
            ))}
          </div>

          {selectedTimeSlot && ( 
            <div className="mt-4">
              <p className="font-semibold">Selected Slot: {selectedTimeSlot}</p>
              <button
                onClick={handleBookingSubmit}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              >
                Book Now
              </button>
            </div>
          )}

          {bookingCode && (
            <div className="mt-4 p-4 bg-green-100 text-green-700 rounded">
              <p className="font-semibold">Booking successful!</p>
              <p>Your booking code: <span className="font-bold">{bookingCode}</span></p>
              <p>Use this code to access your booked room.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
