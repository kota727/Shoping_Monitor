# Shoping_Monitor
# 🛒 AJIO Stock Monitor

Automatically checks AJIO product pages every 10 minutes and sends a **Gmail alert** when your desired size is back in stock. Runs 24/7 on GitHub Actions — no PC needed!

---

## ⚙️ How It Works

- GitHub Actions runs the script every 10 minutes
- The script visits each product page and checks if the target size is available
- If the size is found → an email alert is sent to your Gmail instantly
- Resets automatically if the item goes out of stock again

---

## 📦 Currently Monitoring

| Product | Size | Status |
|---------|------|--------|
| Lee Cooper Men Lace-Up Shoes (Black) | 11 | 🟢 Active |

---

## ➕ How to Add a New Product

1. Go to your repository and click on **`ajio_monitor.py`**
2. Click the **✏️ pencil icon** (Edit) at the top right
3. Find this section near the top:

```python
PRODUCT_URL = "https://www.ajio.com/lee-cooper-men-lace-up-shoes/p/450157154_black"
TARGET_SIZE = "11"
```

4. To monitor **one product**, just change the URL and size:

```python
PRODUCT_URL = "https://www.ajio.com/your-new-product-url"
TARGET_SIZE = "9"   # change to your desired size
```

5. To monitor **multiple products at once**, replace those two lines with a list:

```python
PRODUCTS = [
    {"url": "https://www.ajio.com/lee-cooper-men-lace-up-shoes/p/450157154_black", "size": "11"},
    {"url": "https://www.ajio.com/some-other-product/p/123456789_red", "size": "9"},
    {"url": "https://www.ajio.com/another-product/p/987654321_blue", "size": "42"},
]
```

Then scroll down in the script and replace the `monitor()` function with:

```python
def monitor():
    for product in PRODUCTS:
        log.info(f"Checking: {product['url']} | Size: {product['size']}")
        html = fetch_page(product["url"])
        if html:
            if is_size_available(html, product["size"]):
                log.info(f"Size {product['size']} AVAILABLE! Sending alert...")
                send_email_alert(product["url"], product["size"])
            else:
                log.info(f"Size {product['size']} not available yet.")
        else:
            log.warning("Could not fetch page.")
```

6. Click **"Commit changes"** → **"Commit changes"** again ✅

---

## ➖ How to Remove a Product

1. Open **`ajio_monitor.py`** → click ✏️ Edit
2. Simply **delete** the line with the product URL you no longer want to monitor
3. Click **"Commit changes"** ✅

---

## ⏸️ How to Pause the Monitor

1. Go to **Actions** tab
2. Click **"AJIO Stock Monitor"** on the left
3. Click the **"..."** menu → click **"Disable workflow"**
4. To resume → same steps → click **"Enable workflow"**

---

## 🔁 How to Change Check Frequency

1. Open **`.github/workflows/monitor.yml`** → click ✏️ Edit
2. Find this line:

```yaml
- cron: '*/10 * * * *'   # every 10 minutes
```

3. Change it to your preferred frequency:

| Cron Value | Frequency |
|------------|-----------|
| `*/10 * * * *` | Every 10 minutes |
| `*/30 * * * *` | Every 30 minutes |
| `0 * * * *` | Every 1 hour |
| `0 */6 * * *` | Every 6 hours |

4. Click **"Commit changes"** ✅

---

## 🔐 Secrets Used

| Secret Name | Description |
|-------------|-------------|
| `GMAIL_SENDER` | Gmail address used to send alerts |
| `GMAIL_APP_PASS` | 16-character Gmail App Password |
| `NOTIFY_EMAIL` | Gmail address that receives alerts |

> To update secrets: Go to **Settings** → **Secrets and variables** → **Actions**

---

## ⚠️ Important Notes

- GitHub may **pause the workflow after 60 days** of no commits. If that happens, go to the Actions tab and re-enable it.
- Make sure to use the **full AJIO product URL** (not short links like `ajioapps.onelink.me/...`)
- Gmail App Password is **not** your regular Gmail password. [Generate one here](https://myaccount.google.com/apppasswords)
