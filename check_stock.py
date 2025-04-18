import os
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time

# Load Twilio creds from environment
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE = os.environ["TWILIO_PHONE"]
YOUR_PHONE = os.environ["YOUR_PHONE"]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Replace with the actual URL of the Labubus product
URL = "https://popmart.com.au/products/labubu-xxxx"  # <- update this

def is_in_stock():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return "Sold Out" not in soup.text  # Change if Popmart uses different words

def send_whatsapp_message():
    message = client.messages.create(
        from_="whatsapp:" + TWILIO_PHONE,
        to="whatsapp:" + YOUR_PHONE,
        body="🔥 LABUBU is in stock at Popmart! Go go go!\n" + URL
    )
    print("Sent alert:", message.sid)

while True:
    try:
        if is_in_stock():
            send_whatsapp_message()
            time.sleep(3600)  # wait an hour before checking again
        else:
            print("Still sold out. Checking again in 5 minutes.")
            time.sleep(300)
    except Exception as e:
        print("Error:", e)
        time.sleep(300)
