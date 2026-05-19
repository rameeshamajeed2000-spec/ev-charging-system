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
        password="",   # XAMPP default
        database="ev_charging"
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
# ADD STATION (optional future use)
# =========================
@app.route("/api/stations", methods=["POST"])
def add_station():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO stations (name, location, status) VALUES (%s, %s, %s)",
        (data["name"], data["location"], data["status"])
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

    cursor.execute(
        "INSERT INTO bookings (station_id, user, message) VALUES (%s, %s, %s)",
        (
            data["station_id"],
            data["user"],
            "Slot booked successfully ⚡"
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Booking saved in database ⚡"})

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
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)