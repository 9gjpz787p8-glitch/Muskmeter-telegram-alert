import os, re, time, requests

URL = "https://www.muskmeter.live/?start=1771261200&end=1771434000&eventId=209120&eventType=2-day&source=1"

TOKEN = os.getenv("TG_TOKEN")
CHAT  = os.getenv("TG_CHAT")

def send(msg):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT, "text": msg},
        timeout=20
    )

last = None

while True:
    html = requests.get(URL, timeout=20).text
    m = re.search(r'Event Total[^0-9]{0,80}(\d+)', html, re.I | re.S)

    if m:
        v = int(m.group(1))
        if last is not None and v != last:
            send(f"MuskMeter update: {last} → {v}")
        last = v

    time.sleep(30)
