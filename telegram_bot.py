#!/usr/bin/env python3
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config.config import TELEGRAM_BOT_TOKEN
from src.vehicle_manager import VehicleManager

# Initialize vehicle manager
vm = VehicleManager('data/vehicles_mixed.json')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚛 Welcome to Diesel Tank Monitoring Bot!\n\n"
        "Commands:\n"
        "/vehicles - View all vehicles\n"
        "/fuel VEHICLE_ID - Check fuel level\n"
        "/add VEHICLE_ID FUEL_LEVEL - Add vehicle\n"
        "/update VEHICLE_ID FUEL_LEVEL - Update fuel\n"
        "/alert - Send test alert"
    )

async def vehicles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not vm.vehicles:
        await update.message.reply_text("No vehicles registered.")
        return
    
    message = "🚛 VEHICLE STATUS:\n\n"
    for vehicle_id, data in vm.vehicles.items():
        if data['readings']:
            fuel = data['readings'][-1]['fuel_level']
            status = "🟢 ACTIVE" if fuel > 20 else "🔴 LOW FUEL"
        else:
            fuel = "No data"
            status = "⚪ INACTIVE"
        
        message += f"{vehicle_id}: {fuel}% {status}\n"
        if data.get('destination'):
            message += f"  📍 → {data['destination']}\n"
        message += "\n"
    
    await update.message.reply_text(message)

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /fuel VEHICLE_ID")
        return
    
    vehicle_id = context.args[0].upper()
    if vehicle_id not in vm.vehicles:
        await update.message.reply_text(f"Vehicle {vehicle_id} not found.")
        return
    
    data = vm.vehicles[vehicle_id]
    if data['readings']:
        fuel = data['readings'][-1]['fuel_level']
        liters = fuel * 2.0
        await update.message.reply_text(
            f"⛽ {vehicle_id} FUEL STATUS:\n"
            f"Level: {fuel:.1f}%\n"
            f"Liters: {liters:.1f}L\n"
            f"Date: {data['readings'][-1]['date']}"
        )
    else:
        await update.message.reply_text(f"No fuel data for {vehicle_id}")

async def add_vehicle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /add VEHICLE_ID FUEL_LEVEL")
        return
    
    vehicle_id = context.args[0].upper()
    try:
        fuel_level = float(context.args[1])
        if vm.register_vehicle(vehicle_id):
            vm.record_daily_update(vehicle_id, fuel_level)
            await update.message.reply_text(f"✅ Added {vehicle_id} with {fuel_level}% fuel")
        else:
            await update.message.reply_text(f"❌ Failed to add {vehicle_id} (may exist)")
    except ValueError:
        await update.message.reply_text("❌ Invalid fuel level")

async def update_fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /update VEHICLE_ID FUEL_LEVEL")
        return
    
    vehicle_id = context.args[0].upper()
    try:
        fuel_level = float(context.args[1])
        if vm.record_daily_update(vehicle_id, fuel_level):
            await update.message.reply_text(f"✅ Updated {vehicle_id} to {fuel_level}%")
        else:
            await update.message.reply_text(f"❌ Failed to update {vehicle_id}")
    except ValueError:
        await update.message.reply_text("❌ Invalid fuel level")

async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alert_msg = """🚨 FUEL THEFT ALERT 🚨

Vehicle: TRUCK001
Previous: 85.7%
Current: 15.2%
Drop: 70.5%
Time: Critical

⚠️ IMMEDIATE ATTENTION REQUIRED!"""
    
    await update.message.reply_text(alert_msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if "fuel" in text or "level" in text:
        await update.message.reply_text("Use /vehicles to see all fuel levels or /fuel VEHICLE_ID for specific vehicle")
    elif "help" in text:
        await start(update, context)
    else:
        await update.message.reply_text("Use /start to see available commands")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vehicles", vehicles))
    app.add_handler(CommandHandler("fuel", fuel))
    app.add_handler(CommandHandler("add", add_vehicle))
    app.add_handler(CommandHandler("update", update_fuel))
    app.add_handler(CommandHandler("alert", alert))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Telegram bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()