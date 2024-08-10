"use client";
import React, { useState, useEffect } from "react";
import axios from "axios";
import Link from "next/link";

export default function Home() {
  const [rooms, setRooms] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(searchQuery);
    }, 500); // Wait for 500ms before setting the debounced query

    return () => {
      clearTimeout(handler); // Clear the timeout if searchQuery changes before 500ms
    };
  }, [searchQuery]);

  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/rooms", {
          params: {
            q: debouncedQuery,
          },
        });
        setRooms(response.data);
      } catch (error) {
        console.error("Error fetching rooms:", error);
      }
    };
    fetchRooms();
  }, [debouncedQuery]);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  return (
    <div className="container mx-auto p-4 max-w-screen-lg">
      <h1 className="text-3xl font-bold mb-4">Available Rooms</h1>
      <input
        type="text"
        value={searchQuery}
        onChange={handleSearchChange}
        placeholder="Search rooms..."
        className="mb-4 p-2 border border-gray-300 rounded-md w-full text-black"
      />
      <ul className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {rooms.map((room) => (
          <li key={room.id} className="bg-white rounded-lg shadow-md p-4">
            <Link
              href={`/rooms/${room.id}`}
              className="text-lg font-semibold hover:underline text-black"
            >
              {room.name}
            </Link>
            <p className="text-gray-600">Capacity: {room.capacity}</p>
            <p className="text-gray-600">
              Projector: {room.projector ? "Yes" : "No"}
            </p>
            <p className="text-gray-600">
              Sound System: {room.sound ? "Yes" : "No"}
            </p>
            <div className="mt-4">
              <h3 className="text-md font-semibold text-gray-700">Available Slots:</h3>
              {room.available_slots && room.available_slots.length > 0 ? (
                <p className="text-green-500">Available</p>
              ) : (
                <p className="text-red-500">Not Available</p>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
