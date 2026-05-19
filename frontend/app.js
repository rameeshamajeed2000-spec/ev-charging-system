import { useEffect, useState } from "react";
import API from "./services/api";

function App() {
  const [stations, setStations] = useState([]);
  const [bookings, setBookings] = useState([]);

  // =========================
  // FETCH STATIONS
  // =========================
  const getStations = () => {
    API.get("/api/stations")
      .then((res) => setStations(res.data))
      .catch((err) => console.log(err));
  };

  // =========================
  // FETCH BOOKINGS
  // =========================
  const getBookings = () => {
    API.get("/api/bookings")
      .then((res) => setBookings(res.data))
      .catch((err) => console.log(err));
  };

  // =========================
  // BOOK SLOT
  // =========================
  const bookSlot = (stationId) => {
    API.post("/api/bookings", {
      station_id: stationId,
      user: "Rameesha"
    })
      .then((res) => {
        alert(res.data.message);
        getBookings(); // refresh bookings after booking
      })
      .catch((err) => console.log(err));
  };

  // =========================
  // LOAD DATA ON PAGE LOAD
  // =========================
  useEffect(() => {
    getStations();
    getBookings();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>EV Charging Station System ⚡🚗</h1>

      {/* =========================
          STATIONS SECTION
      ========================= */}
      <h2>Available Stations</h2>

      {stations.map((station) => (
        <div
          key={station.id}
          style={{
            border: "1px solid gray",
            margin: "10px",
            padding: "10px",
            borderRadius: "8px"
          }}
        >
          <h3>{station.name}</h3>
          <p>📍 {station.location}</p>
          <p>⚡ Status: {station.status}</p>

          <button onClick={() => bookSlot(station.id)}>
            Book Slot
          </button>
        </div>
      ))}

      {/* =========================
          BOOKINGS SECTION
      ========================= */}
      <h2>My Bookings</h2>

      {bookings.length === 0 ? (
        <p>No bookings yet</p>
      ) : (
        bookings.map((b) => (
          <div
            key={b.id}
            style={{
              border: "1px solid green",
              margin: "10px",
              padding: "10px",
              borderRadius: "8px"
            }}
          >
            <p>Booking ID: {b.id}</p>
            <p>User: {b.user}</p>
            <p>{b.message}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default App;