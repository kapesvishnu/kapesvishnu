#!/usr/bin/env python3
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config.config import TELEGRAM_BOT_TOKEN
from src.vehicle_manager import VehicleManager
import requests

# Initialize vehicle manager
vm = VehicleManager('data/vehicles_mixed.json')

async def sms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send SMS to vehicle driver: /sms VEHICLE_ID MESSAGE"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /sms VEHICLE_ID MESSAGE\nExample: /sms VEHICLE001 Check fuel level immediately")
        return
    
    vehicle_id = context.args[0].upper()
    message = ' '.join(context.args[1:])
    
    if vehicle_id not in vm.vehicles:
        await update.message.reply_text(f"❌ Vehicle {vehicle_id} not found")
        return
    
    vehicle_data = vm.vehicles[vehicle_id]
    phone = vehicle_data.get('phone')
    
    if not phone:
        await update.message.reply_text(f"❌ No phone number for {vehicle_id}")
        return
    
    # Send SMS via dashboard API
    dashboard_url = "http://localhost:8080/send_sms"
    sms_data = {
        'vehicle_id': vehicle_id,
        'phone': phone,
        'message': message,
        'sender': 'Telegram Bot'
    }
    
    try:
        response = requests.post(dashboard_url, json=sms_data)
        if response.status_code == 200:
            await update.message.reply_text(f"✅ SMS sent to {vehicle_id} ({phone})\nMessage: {message}")
        else:
            # Fallback: Show SMS format
            await update.message.reply_text(f"📱 SMS TO {vehicle_id}\nPhone: {phone}\nMessage: {message}\n\n⚠️ Dashboard offline - SMS queued")
    except:
        # Show SMS details for manual sending
        await update.message.reply_text(f"📱 SMS TO {vehicle_id}\nPhone: {phone}\nMessage: {message}\n\n📋 Copy and send manually")

async def fuel_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send fuel check SMS: /fuelsms VEHICLE_ID"""
    if not context.args:
        await update.message.reply_text("Usage: /fuelsms VEHICLE_ID")
        return
    
    vehicle_id = context.args[0].upper()
    message = f"🚛 FUEL CHECK REQUIRED\n\nVehicle: {vehicle_id}\nPlease check fuel level and report immediately.\n\nFrom: Diesel Monitoring System"
    
    # Use the sms command
    context.args = [vehicle_id] + message.split()
    await sms_command(update, context)

async def emergency_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send emergency SMS: /emergency VEHICLE_ID"""
    if not context.args:
        await update.message.reply_text("Usage: /emergency VEHICLE_ID")
        return
    
    vehicle_id = context.args[0].upper()
    message = f"🚨 EMERGENCY ALERT\n\nVehicle: {vehicle_id}\nIMMEDIATE RESPONSE REQUIRED\nContact control room: +91 9876543210\n\nUrgent: Diesel Monitoring System"
    
    context.args = [vehicle_id] + message.split()
    await sms_command(update, context)

async def broadcast_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send SMS to all vehicles: /broadcast MESSAGE"""
    if not context.args:
        await update.message.reply_text("Usage: /broadcast MESSAGE")
        return
    
    message = ' '.join(context.args)
    sent_count = 0
    
    for vehicle_id, data in vm.vehicles.items():
        if data.get('phone'):
            context.args = [vehicle_id] + message.split()
            await sms_command(update, context)
            sent_count += 1
            await asyncio.sleep(1)  # Avoid spam
    
    await update.message.reply_text(f"📡 Broadcast sent to {sent_count} vehicles")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚛 Diesel Tank SMS Bot\n\n"
        "SMS Commands:\n"
        "/sms VEHICLE_ID MESSAGE - Send custom SMS\n"
        "/fuelsms VEHICLE_ID - Send fuel check SMS\n"
        "/emergency VEHICLE_ID - Send emergency alert\n"
        "/broadcast MESSAGE - Send to all vehicles\n\n"
        "Examples:\n"
        "/sms VEHICLE001 Report your location\n"
        "/fuelsms VEHICLE002\n"
        "/emergency VEHICLE001"
    )

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sms", sms_command))
    app.add_handler(CommandHandler("fuelsms", fuel_sms))
    app.add_handler(CommandHandler("emergency", emergency_sms))
    app.add_handler(CommandHandler("broadcast", broadcast_sms))
    
    print("🤖 Telegram SMS Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()