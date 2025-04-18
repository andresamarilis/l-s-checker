import os
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time

# Twilio credentials from Railway environment variables
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = os.environ["TWILIO_PHONE"]
YOUR_PHONE = os.environ["YOUR_PHONE"]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# 4 products, including 1 that is confirmed IN STOCK
PRODUCTS = {
    "Checkmate Pendant": "https://au.popmart.com/collections/the-monsters/products/pop-mart-the-monsters-labubu-lets-checkmate-vinyl-plush-pendant",
    "Have A Seat Blind Box": "https://au.popmart.com/collections/the-monsters/products/pop-mart-the-monsters-have-a-seat-series-plush-pendant-blind-box",
    "Exciting Macaron Blind Box": "https://au.popmart.com/collections/the-monsters/products/pop-mart-the-monsters-exciting-macaron-series-plush-pendant-blind-box",
    "Drunk in Sea Magnet Box": "https://au.popmart.com/products/pop-mart-the-monsters-labubu-drunk-in-sea-series-fridge-magnet-blind-box"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_in_stock(url):
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        return "ADD TO CART" in soup.text.upper()
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

def send_whatsapp_message(name, url):
    message = client.messages.create(
        from_="whatsapp:" + TWILIO_PHONE,
        to="whatsapp:" + YOUR_PHONE,
        body=f"🔥 {name} is IN STOCK at Popmart!\n{url}"
    )
    print(f"Sent alert for {name} - SID: {message.sid}")

    print(" Restarting stock check")


# Main loop
while True:
    try:
        for name, url in PRODUCTS.items():
            print(f"Checking: {name}")
            if is_in_stock(url):
                send_whatsapp_message(name, url)
            else:
                print(f"{name}: Still sold out.")
        print("Sleeping for 5 minutes...")
        time.sleep(300)
    except Exception as e:
        print("General error:", e)
        time.sleep(300)
