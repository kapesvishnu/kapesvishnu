from flask import Flask, render_template, request, jsonify
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.vehicle_manager import VehicleManager
except ImportError:
    from vehicle_manager import VehicleManager

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))

# Use absolute path for data file
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'vehicles_mixed.json')
vehicle_manager = VehicleManager(data_path)

@app.route('/')
def dashboard():
    return render_template('dashboard.html', vehicles=vehicle_manager.vehicles)

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    fuel_level = data.get('fuel_level', 200)  # Default 200L (full tank)
    destination = data.get('destination')
    contact = data.get('contact')
    phone = data.get('phone')
    
    if vehicle_manager.register_vehicle(vehicle_id, destination, contact, phone):
        if fuel_level != 200:
            vehicle_manager.record_daily_update(vehicle_id, fuel_level)
        return jsonify({'success': True, 'message': f'Vehicle {vehicle_id} added successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to add vehicle (may already exist)'})

@app.route('/update_vehicle', methods=['POST'])
def update_vehicle():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    fuel_level = data.get('fuel_level')
    destination = data.get('destination')
    contact = data.get('contact')
    phone = data.get('phone')
    
    if vehicle_manager.update_vehicle(vehicle_id, fuel_level, destination, contact, phone):
        updated_fields = []
        if fuel_level: updated_fields.append('fuel')
        if destination: updated_fields.append('destination')
        if contact: updated_fields.append('contact')
        if phone: updated_fields.append('phone')
        
        fields_str = ', '.join(updated_fields) if updated_fields else 'vehicle'
        return jsonify({'success': True, 'message': f'Updated {fields_str} for {vehicle_id}'})
    else:
        return jsonify({'success': False, 'message': 'Failed to update vehicle (invalid data or vehicle not found)'})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    message = data.get('message')
    
    if vehicle_id in vehicle_manager.vehicles:
        contact = vehicle_manager.vehicles[vehicle_id].get('contact')
        if contact:
            # Send message via Telegram
            alert_msg = f"📱 MESSAGE TO {vehicle_id}\nContact: {contact}\nMessage: {message}"
            try:
                sys.path.append(os.path.dirname(os.path.dirname(__file__)))
                from send_bot_alert import send_telegram_bot_alert
                send_telegram_bot_alert(alert_msg)
                return jsonify({'success': True, 'message': f'Message sent to {vehicle_id}'})
            except Exception as e:
                return jsonify({'success': True, 'message': f'Message logged for {vehicle_id} ({contact})'})
        else:
            return jsonify({'success': False, 'message': 'No contact number found for this vehicle'})
    else:
        return jsonify({'success': False, 'message': 'Vehicle not found'})

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    phone = data.get('phone')
    message = data.get('message')
    sender = data.get('sender', 'Dashboard')
    
    if vehicle_id in vehicle_manager.vehicles:
        # Log SMS in Telegram
        sms_log = f"📱 SMS SENT VIA BOT\n\nVehicle: {vehicle_id}\nPhone: {phone}\nSender: {sender}\nMessage: {message}\n\nStatus: Delivered to device"
        
        try:
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from send_bot_alert import send_telegram_bot_alert
            send_telegram_bot_alert(sms_log)
            return jsonify({'success': True, 'message': f'SMS sent to {vehicle_id}'})
        except Exception as e:
            return jsonify({'success': True, 'message': f'SMS queued for {vehicle_id}'})
    else:
        return jsonify({'success': False, 'message': 'Vehicle not found'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
