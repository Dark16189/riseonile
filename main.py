import os
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_TOKEN")
SMM_API_KEY = os.getenv("SMM_KEY")
SMM_API_URL = os.getenv("API_URL", "https://smmgalaxy.com/api/v2")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def get_balance():
    response = requests.post(SMM_API_URL, data={
        "key": SMM_API_KEY,
        "action": "balance"
    })
    return response.json().get("balance", 0)

@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != TOKEN:
        return {"status": "unauthorized"}

    data = await request.json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").lower()

    if text == "/start":
        send_message(chat_id, "👋 Welcome to Rise Online Bot!
Choose a platform to get started:
➡️ Instagram
➡️ YouTube")

    elif "instagram" in text:
        send_message(chat_id, "Choose a service for Instagram:
1. Followers
2. Likes
3. Comments
4. Views
5. Engagement")

    elif "youtube" in text:
        send_message(chat_id, "Choose a service for YouTube:
1. Views
2. Subscribers
3. Likes
4. Comments")

    elif "followers" in text or "likes" in text or "comments" in text or "views" in text:
        send_message(chat_id, "Enter quantity (e.g., 100):")

    elif text.isdigit():
        quantity = int(text)
        price = quantity * 0.18
        send_message(chat_id, f"💰 Total: ₹{price:.2f}
Pay to UPI: 8188938018@fam or scan the QR code.
Then send your screenshot.")

        # Check SMM balance
        balance = float(get_balance())
        if balance < 10 or balance < price:
            alert = f"⚠️ Low funds alert!
Current balance: ₹{balance:.2f}
Required: ₹{price:.2f}"
            send_message(ADMIN_CHAT_ID, alert)

    elif "screenshot" in text or text.startswith("utr"):
        send_message(chat_id, "✅ Screenshot received. Admin will verify and place your order.
If you face any issue, contact @riseonlineofficial")
    else:
        send_message(chat_id, "Send /start to begin.")

    return {"ok": True}
