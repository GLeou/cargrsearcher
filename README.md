# 🔍 Car.gr Ad Tracker (Telegram Notifier)

This Python script monitors **Car.gr** listings for new ads (e.g. motorcycles, cars, boats, bicycles, parts, plots) based on a custom search URL. When a new ad appears, it sends an instant **Telegram message**.

---

## 🚀 Features

- Monitors any Car.gr ad category (`bikes`, `cars`, `boats`, `bicycles`, `parts`, `plot`)
- Sends a Telegram notification for each **new ad**
- Remembers previously sent ads (`seen_ids.txt`)
- Uses **Selenium + headless Chrome** to bypass scraping protection
- Works continuously in the background

---

## ✅ Requirements

- Python 3.7+
- Google Chrome installed
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) (matching your Chrome version)
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Your personal Telegram Chat ID

---

## 📦 Installation

Install dependencies:

```bash
pip install selenium requests
```

Download the matching [ChromeDriver](https://sites.google.com/chromium.org/driver/) and place it:
- in the same folder as the script, or
- somewhere in your system's PATH

---

## 🔧 Configuration

Open `tracker.py` and edit these variables:

```python
SEARCH_URL = "YOUR CAR.GR URL"
TELEGRAM_TOKEN = "YOUR TELEGRAM BOT TOKEN"
TELEGRAM_CHAT_ID = "YOUR CHAT ID"
```

> ⚠️ If you change the category in the URL (e.g. from `bikes` to `cars`), make sure the regex in `fetch_ads()` matches it too.

Example:
```python
re.findall(r"/classifieds/cars/view/(\d+)", html)
```

---

## 📬 How to Get Your Chat ID

1. Open your bot on Telegram and send a message (e.g. `/start`)
2. Visit:  
   `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Find the `"chat": { "id": ... }` — that number is your `chat_id`

---

## ▶️ Run the Script

```bash
python tracker.py
```

It will check for new ads every `CHECK_INTERVAL` seconds (default is 300 seconds = 5 minutes).

---

## 🗂 Generated Files

- `seen_ids.txt`: stores previously sent ad IDs
- `cargr_response_selenium.html` *(optional)*: raw HTML snapshot for debugging

---

## 🛑 To Stop the Script

Use `Ctrl + C` in the terminal.

---

## ⚠️ Notes

- Avoid scraping too frequently — stick to 60–300 seconds between checks
- **Do not push your Telegram token to GitHub** — use a `.env` file or secret variables for deployment

---

## 📄 License

This project is provided "as is" for personal and educational use.
