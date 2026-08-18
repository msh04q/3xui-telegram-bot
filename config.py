import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройки 3X-UI
XUI_URL = os.getenv("XUI_URL", "http://127.0.0.1:2096").rstrip("/")
XUI_BASE_PATH = os.getenv("XUI_BASE_PATH", "/").strip("/")
if XUI_BASE_PATH:
    XUI_BASE_PATH = f"/{XUI_BASE_PATH}"

XUI_USERNAME = os.getenv("XUI_USERNAME", "mik-admin")
XUI_PASSWORD = os.getenv("XUI_PASSWORD", "")
INBOUND_ID = int(os.getenv("INBOUND_ID", 1))

# Настройки VLESS REALITY
VLESS_SERVER = os.getenv("VLESS_SERVER", "")
VLESS_PORT = int(os.getenv("VLESS_PORT", 443))
