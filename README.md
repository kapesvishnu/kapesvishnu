# Diesel Tank Monitoring System

This project is a diesel tank monitoring system that provides notifications for sudden fuel drops, tracks vehicle location, and offers a local dashboard for monitoring.

## Features

- **Tank Monitoring:** Simulates fuel tank readings and detects sudden drops.
- **Notifications:** Sends alerts via Telegram and email for sudden fuel drops.
- **Vehicle Management:** Allows registration of vehicles and stores daily fuel readings.
- **Location Tracking:** Simulates live vehicle location tracking and estimates mileage.
- **Local Dashboard:** A web-based dashboard to monitor vehicle data locally.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application:**
   - Open `config/config.py` and update the following values with your credentials:
     - `TELEGRAM_BOT_TOKEN`
     - `TELEGRAM_CHAT_ID`
     - `EMAIL_HOST`
     - `EMAIL_PORT`
     - `EMAIL_USER`
     - `EMAIL_PASSWORD`
     - `EMAIL_RECIPIENT`

## Running the Application

- **To run the dashboard:**
  ```bash
  python src/dashboard.py
  ```
  The dashboard will be available at `http://127.0.0.1:5000`.

- **To run the tests:**
  ```bash
  python -m unittest discover tests
  ```
