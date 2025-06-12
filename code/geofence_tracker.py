import requests
import telegram
import folium
import asyncio
from flask import Flask, render_template
from datetime import datetime
from time import sleep
from threading import Thread

# ✅ Firebase Database URL (Users should replace this with their own)
FIREBASE_URL = "YOUR_FIREBASE_URL"

# ✅ Telegram Bot Credentials (Users should replace these with their own)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

# Initialize Flask App
app = Flask(__name__)

# Initialize Telegram Bot
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def fetch_latest_geofence_data():
    """Fetch the latest asset location from Firebase."""
    response = requests.get(FIREBASE_URL)

    if response.status_code == 200:
        data = response.json()

        if not data:
            print("⚠️ No valid data available in Firebase.")
            return None

        # Extract and sort entries by timestamp
        entries = [
            entry for entry in data.values()
            if "timestamp" in entry and "latitude" in entry and "longitude" in entry
        ]

        if not entries:
            print("⚠️ No valid geofencing entries found.")
            return None

        # Sort entries by timestamp (latest first)
        entries.sort(key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"), reverse=True)

        # Get the latest geofencing entry
        return entries[0]
    else:
        print("⚠️ Error fetching data from Firebase.")
        return None

async def send_telegram_alert(latest_data):
    """Send Telegram alert asynchronously."""
    message = (
        f"📍 Geofence Alert:\n"
        f"🌍 Latitude: {latest_data['latitude']}\n"
        f"🌍 Longitude: {latest_data['longitude']}\n"
        f"📏 Distance: {latest_data.get('distance', 'N/A')}m\n"
        f"🔴 Status: {latest_data.get('status', 'Unknown')}\n"
        f"🕒 Timestamp: {latest_data['timestamp']}"
    )

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

@app.route('/')
def show_map():
    """Generate Google Maps visualization for real-time tracking."""
    latest_data = fetch_latest_geofence_data()
    if latest_data:
        map = folium.Map(location=[latest_data["latitude"], latest_data["longitude"]], zoom_start=15)

        folium.Marker(
            [latest_data["latitude"], latest_data["longitude"]],
            popup=f"📍 Status: {latest_data.get('status', 'Unknown')}",
            icon=folium.Icon(color="red" if latest_data.get("status") == "OUTSIDE Geofence" else "green")
        ).add_to(map)

        return map._repr_html_()
    return "⚠️ No valid geofencing data available"

def telegram_alerts_thread():
    """Continuously fetch Firebase data and send alerts."""
    previous_data = None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        latest_data = fetch_latest_geofence_data()

        if latest_data:
            loop.run_until_complete(send_telegram_alert(latest_data))

            if previous_data is None or latest_data["timestamp"] != previous_data["timestamp"]:
                previous_data = latest_data
                print(f"🔄 New Firebase Data Updated: {latest_data}")

        sleep(1)  # Sends alerts every 1 second

# Start Telegram alerts in the background
Thread(target=telegram_alerts_thread).start()

# Start Flask for live tracking dashboard
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)