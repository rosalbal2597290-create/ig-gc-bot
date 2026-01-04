
# =====================================
# Instagram GC Welcome + Mini-AI Bot
# Photo support + mention only
# Owner: @rahul.xp199
# =====================================

from instagrapi import Client
import time, random, os
from datetime import date

IG_USERNAME = "Mumux9"
IG_PASSWORD = "Termuxterminal"

BOT_USERNAME = "mumux9"
OWNER_USERNAME = "rahul.xp199"

PHOTO_DIR = "photos"

INTRO_PHOTOS = []
SUPPORT_PHOTOS = []

for f in os.listdir(PHOTO_DIR):
    if f.lower().startswith("intro"):
        INTRO_PHOTOS.append(os.path.join(PHOTO_DIR, f))
    elif f.lower().startswith("support"):
        SUPPORT_PHOTOS.append(os.path.join(PHOTO_DIR, f))

INTRO_TEXT = (
    "👋 *Intro*\n"
    "Main GC smart assistant hoon 🤍\n"
    "Mention karoge to hi reply karti hoon 😌\n"
    "Owner: @rahul.xp199"
)

SUPPORT_TEXT = (
    "🆘 *Support & Contact*\n\n"
    "👤 Owner: Rahul\n"
    "📱 WhatsApp: +62 831-7683-2295\n"
    "📧 Email: rosalbal2597290@gmail.com\n"
    "📸 Instagram: @rahul.xp199"
)

WELCOME_MESSAGES = [
    "Heyy @{user} 👋 welcome 💖",
    "Hii @{user} 😊 welcome to the gc",
    "Hey @{user} ✨ enjoy here",
]

def connect():
    while True:
        try:
            cl = Client()
            cl.login(IG_USERNAME, IG_PASSWORD)
            print("✅ Instagram connected")
            return cl
        except Exception as e:
            print("Login error, retrying...", e)
            time.sleep(15)

cl = connect()
welcomed = set()
today = date.today()

print("🤖 Bot started with PHOTO support")

while True:
    try:
        if date.today() != today:
            welcomed.clear()
            today = date.today()

        threads = cl.direct_threads(amount=5)

        for t in threads:
            if not t.is_group:
                continue

            msgs = cl.direct_messages(t.id, amount=1)
            if not msgs or not msgs[0].text:
                continue

            msg = msgs[0]
            text = msg.text.lower()

            if f"@{BOT_USERNAME}" not in text:
                continue

            user = next((u.username for u in t.users if u.pk == msg.user_id), None)
            if not user:
                continue

            key = f"{t.id}_{user}"

            if key not in welcomed:
                reply = random.choice(WELCOME_MESSAGES).format(user=user)
                cl.direct_send(reply, thread_ids=[t.id])
                welcomed.add(key)
                continue

            if "intro" in text:
                if INTRO_PHOTOS:
                    cl.direct_send_photo(
                        INTRO_PHOTOS[random.choice(range(len(INTRO_PHOTOS)))],
                        thread_ids=[t.id],
                        caption=INTRO_TEXT
                    )
                else:
                    cl.direct_send(INTRO_TEXT, thread_ids=[t.id])

            elif "support" in text or "contact" in text:
                if SUPPORT_PHOTOS:
                    cl.direct_send_photo(
                        SUPPORT_PHOTOS[random.choice(range(len(SUPPORT_PHOTOS)))],
                        thread_ids=[t.id],
                        caption=SUPPORT_TEXT
                    )
                else:
                    cl.direct_send(SUPPORT_TEXT, thread_ids=[t.id])

        time.sleep(3)

    except Exception as e:
        print("Error / reconnecting:", e)
        time.sleep(10)
        cl = connect()
