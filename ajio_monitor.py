import requests
import smtplib
import time
import logging
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

PRODUCT_URL = "https://www.ajio.com/lee-cooper-men-lace-up-shoes/p/450157154_black"
TARGET_SIZE = "11"

GMAIL_SENDER   = os.environ["GMAIL_SENDER"]
GMAIL_APP_PASS = os.environ["GMAIL_APP_PASS"]
NOTIFY_EMAIL   = os.environ["NOTIFY_EMAIL"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        log.error(f"Failed to fetch page: {e}")
        return None


def is_size_available(html, size):
    size_positions = [m.start() for m in re.finditer(r'\b' + re.escape(size) + r'\b', html)]
    for pos in size_positions:
        context = html[max(0, pos - 200): pos + 50].lower()
        if size.lower() in context:
            if "soldout" not in context and "out-of-stock" not in context and "disabled" not in context:
                log.info(f"Size {size} found available!")
                return True
    return False


def send_email_alert(product_url, size):
    subject = f"AJIO Size {size} is back in stock!"
    body = f"""
Hi there,

Great news! Size {size} is now available on AJIO.

Product link:
{product_url}

Hurry — it may sell out quickly!

Checked at: {datetime.now().strftime("%d %b %Y, %I:%M %p")}

— Your AJIO Stock Monitor
"""
    msg = MIMEMultipart()
    msg["From"]    = GMAIL_SENDER
    msg["To"]      = NOTIFY_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_SENDER, GMAIL_APP_PASS)
            server.sendmail(GMAIL_SENDER, NOTIFY_EMAIL, msg.as_string())
        log.info("Alert email sent successfully!")
    except smtplib.SMTPException as e:
        log.error(f"Failed to send email: {e}")


def monitor():
    log.info(f"Starting monitor | Size: {TARGET_SIZE}")
    log.info(f"Watching: {PRODUCT_URL}")

    html = fetch_page(PRODUCT_URL)
    if html:
        if is_size_available(html, TARGET_SIZE):
            log.info(f"Size {TARGET_SIZE} is AVAILABLE! Sending email...")
            send_email_alert(PRODUCT_URL, TARGET_SIZE)
        else:
            log.info(f"Size {TARGET_SIZE} not available yet.")
    else:
        log.warning("Could not fetch page.")


if __name__ == "__main__":
    monitor()
