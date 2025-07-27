from flask import Flask, render_template, request, jsonify
try:
    from vehicle_manager import VehicleManager
except ImportError:
    from src.vehicle_manager import VehicleManager
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))
vehicle_manager = VehicleManager()

@app.route('/')
def dashboard():
    return render_template('dashboard.html', vehicles=vehicle_manager.vehicles)

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    fuel_level = data.get('fuel_level', 100)
    
    if vehicle_manager.register_vehicle(vehicle_id):
        if fuel_level != 100:
            vehicle_manager.record_daily_update(vehicle_id, fuel_level)
        return jsonify({'success': True, 'message': f'Vehicle {vehicle_id} added successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to add vehicle (may already exist)'})

@app.route('/update_fuel', methods=['POST'])
def update_fuel():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    fuel_level = data.get('fuel_level')
    
    if vehicle_manager.record_daily_update(vehicle_id, fuel_level):
        return jsonify({'success': True, 'message': f'Fuel updated for {vehicle_id}'})
    else:
        return jsonify({'success': False, 'message': 'Failed to update fuel (invalid data or vehicle not found)'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
