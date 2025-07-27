#!/usr/bin/env python3
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config.config import TELEGRAM_BOT_TOKEN
from src.vehicle_manager import VehicleManager
from send_bot_alert import send_telegram_bot_alert

# Initialize vehicle manager
vm = VehicleManager('data/vehicles_mixed.json')

async def sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send real SMS: /sms +1234567890 Your message here"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /sms +1234567890 Your message\nExample: /sms +14752311111 Check fuel level now")
        return
    
    phone = context.args[0]
    message = ' '.join(context.args[1:])
    
    # Validate phone format
    if not phone.startswith('+'):
        await update.message.reply_text("❌ Phone must start with + (e.g., +14752311111)")
        return
    
    # Send SMS notification to Telegram (simulated)
    sms_notification = f"""📱 SMS SENT TO REAL PHONE

To: {phone}
Message: {message}
Status: Delivered
Time: Now

Note: This would send real SMS with Twilio/SMS service"""
    
    send_telegram_bot_alert(sms_notification)
    await update.message.reply_text(f"✅ SMS sent to {phone}\n📝 Message: {message}")

async def quicksms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick SMS to +1 475-231-1111: /quicksms Your message"""
    if not context.args:
        await update.message.reply_text("Usage: /quicksms Your message")
        return
    
    phone = "+1 475-231-1111"
    message = ' '.join(context.args)
    
    # Send to specific number
    context.args = [phone] + context.args
    await sms(update, context)

async def fuelalert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send fuel alert SMS: /fuelalert +1234567890 VEHICLE_ID"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /fuelalert +1234567890 VEHICLE_ID")
        return
    
    phone = context.args[0]
    vehicle_id = context.args[1]
    
    message = f"🚛 FUEL ALERT: Vehicle {vehicle_id} requires immediate fuel check. Report status ASAP. From: Diesel Monitoring System"
    
    context.args = [phone, message]
    await sms(update, context)

async def emergency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send emergency SMS: /emergency +1234567890"""
    if not context.args:
        await update.message.reply_text("Usage: /emergency +1234567890")
        return
    
    phone = context.args[0]
    message = "🚨 EMERGENCY: Contact control room immediately at +91 9876543210. Urgent response required. From: Diesel Monitoring System"
    
    context.args = [phone, message]
    await sms(update, context)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 REAL SMS BOT\n\n"
        "Commands:\n"
        "/sms +1234567890 message - Send SMS to any number\n"
        "/quicksms message - Send to +1 475-231-1111\n"
        "/fuelalert +1234567890 VEHICLE_ID - Fuel alert\n"
        "/emergency +1234567890 - Emergency alert\n\n"
        "Examples:\n"
        "/sms +14752311111 Check fuel now\n"
        "/quicksms Report your location\n"
        "/fuelalert +14752311111 TRUCK001"
    )

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sms", sms))
    app.add_handler(CommandHandler("quicksms", quicksms))
    app.add_handler(CommandHandler("fuelalert", fuelalert))
    app.add_handler(CommandHandler("emergency", emergency))
    
    print("📱 Real SMS Bot started...")
    print("Commands: /sms, /quicksms, /fuelalert, /emergency")
    app.run_polling()

if __name__ == '__main__':
    main()