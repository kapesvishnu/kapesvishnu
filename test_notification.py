#!/usr/bin/env python3
import asyncio
from src.notifications import send_telegram_alert, send_email_alert

async def test_telegram():
    try:
        await send_telegram_alert("🚨 FUEL ALERT: Vehicle TRUCK001 - Sudden fuel drop detected! Current level: 15%")
        print("✓ Telegram alert sent successfully")
    except Exception as e:
        print(f"✗ Telegram alert failed: {e}")

def test_email():
    try:
        send_email_alert(
            "FUEL ALERT - Vehicle TRUCK001", 
            "Sudden fuel drop detected!\n\nVehicle: TRUCK001\nCurrent fuel level: 15%\nPrevious level: 85%\nDrop: 70%\n\nImmediate attention required."
        )
        print("✓ Email alert sent successfully")
    except Exception as e:
        print(f"✗ Email alert failed: {e}")

async def main():
    print("Testing notification alerts...")
    await test_telegram()
    test_email()

if __name__ == '__main__':
    asyncio.run(main())