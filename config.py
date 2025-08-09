from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
DB_URL = os.getenv("DATABASE_URL")
print(DB_URL, os.getenv("DATABASE_URL"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
STRIPE_APIKEY = os.getenv("STRIPE_APIKEY")
FRONTEND_URL = os.getenv("FRONTEND_URL")