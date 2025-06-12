This README provides an overview of the project, installation steps, and setup instructions. All detailed components, including configurations and code, are available in the required components file within the repository.

📌 Project Overview
This project implements an IoT-based asset tracking system with geofencing, integrating:
✅ MATLAB Simulink GPS Generator for simulated movement.
✅ Python Flask Web Dashboard for real-time tracking.
✅ Firebase Realtime Database for asset location storage.
✅ Telegram Bot Notifications for geofence alerts.

🔹 Refer to the required_components.txt file in the repository for full setup details.


🔧 Installation & Setup Guide
1️⃣ Install Dependencies
✅ Install Python & required packages:
pip install -r requirements.txt


✅ Verify Flask installation:
flask --version


2️⃣ Firebase & Telegram Setup
✅ Follow the instructions in required_components.txt to set up:
🔹 Firebase Database
🔹 Telegram Bot Credentials


3️⃣ Running the Flask Tracking System
✅ Navigate to the project directory:
cd GeofenceTracker
python geofence_tracker.py


✅ Open the tracking dashboard in your browser:
👉 http://localhost:5000


