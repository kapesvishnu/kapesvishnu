from flask import Flask, render_template
from src.vehicle_manager import VehicleManager
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))
vehicle_manager = VehicleManager()

@app.route('/')
def dashboard():
    return render_template('dashboard.html', vehicles=vehicle_manager.vehicles)

if __name__ == '__main__':
    app.run(debug=True)
