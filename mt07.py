import time
import re
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# === ΡΥΘΜΙΣΕΙΣ ===
SEARCH_URL = "YOUR CAR.GR URL"
CHECK_INTERVAL = 300  # Κάθε 5 λεπτά
TELEGRAM_TOKEN = "YOUR TELEGRAM TOKEN"
TELEGRAM_CHAT_ID = "YOUR CHAT ID"
SEEN_FILE = "seen_ids.txt"

# === ΑΝΑΓΝΩΣΗ/ΑΠΟΘΗΚΕΥΣΗ ID ===
def load_seen_ids():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_seen_ids(ids):
    with open(SEEN_FILE, "a") as f:
        for ad_id in ids:
            f.write(f"{ad_id}\n")

# === ΑΠΟΣΤΟΛΗ ΣΤΟ TELEGRAM ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"⚠️ Σφάλμα Telegram: {response.text}")

# === ΦΟΡΤΩΣΗ ΑΓΓΕΛΙΩΝ ΜΕ SELENIUM ===
def fetch_ads():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(SEARCH_URL)
    time.sleep(3)

    html = driver.page_source
    driver.quit()

    # Εξαγωγή αγγελιών από HTML
    ids = set(re.findall(r"/classifieds/bikes/view/(\d+)", html))
    print(f"➡️ Βρέθηκαν {len(ids)} αγγελίες.")
    return ids

# === ΚΥΡΙΟ LOOP ===
print("🔍 Παρακολούθηση νέων αγγελιών ξεκίνησε...")
seen_ids = load_seen_ids()

while True:
    try:
        current_ids = fetch_ads()
        new_ids = current_ids - seen_ids
        if new_ids:
            for ad_id in new_ids:
                ad_url = f"https://www.car.gr/classifieds/<CATEGORY_SLUG>/view/{ad_id}"
                send_telegram_message(f"📌 Νέα αγγελία:\n{ad_url}")
                print(f"✅ Εστάλη: {ad_url}")
            seen_ids.update(new_ids)
            save_seen_ids(new_ids)
        else:
            print("🔎 Καμία νέα αγγελία.")
    except Exception as e:
        print(f"❌ Σφάλμα: {e}")
    time.sleep(CHECK_INTERVAL)
