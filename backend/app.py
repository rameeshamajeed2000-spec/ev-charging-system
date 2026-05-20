from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# =========================
# DATABASE CONNECTION
# =========================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",   # XAMPP default
        database="ev_project"
    )

# =========================
# HOME ROUTE
# =========================
@app.route("/")
def home():
    return jsonify({
        "message": "EV Charging API Running with MySQL ⚡"
    })

# =========================
# USER REGISTER
# =========================
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (data["username"], data["password"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully ✅"})

# =========================
# USER LOGIN
# =========================
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (data["username"], data["password"])
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful ✅"})
    else:
        return jsonify({"message": "Invalid credentials ❌"})

# =========================
# GET ALL STATIONS
# =========================
@app.route("/api/stations", methods=["GET"])
def get_stations():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM stations")
    stations = cursor.fetchall()

    conn.close()
    return jsonify(stations)

# =========================
# ADD STATION
# =========================
@app.route("/api/stations", methods=["POST"])
def add_station():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO stations (name, location, total_slots, available_slots) VALUES (%s, %s, %s, %s)",
        (
            data["name"],
            data["location"],
            data["total_slots"],
            data["available_slots"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Station added successfully ⚡"})

# =========================
# BOOK SLOT
# =========================
@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    # insert booking
    cursor.execute(
        "INSERT INTO bookings (station_id, user, message) VALUES (%s, %s, %s)",
        (
            data["station_id"],
            data["user"],
            "Slot booked successfully ⚡"
        )
    )

    # reduce available slots
    cursor.execute(
        "UPDATE stations SET available_slots = available_slots - 1 WHERE id = %s",
        (data["station_id"],)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Booking successful ⚡"})

# =========================
# GET ALL BOOKINGS
# =========================
@app.route("/api/bookings", methods=["GET"])
def get_bookings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    conn.close()
    return jsonify(bookings)

# =========================
# DELETE BOOKING (NEW)
# =========================
@app.route("/api/bookings/<int:id>", methods=["DELETE"])
def delete_booking(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Booking deleted 🗑️"})

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)