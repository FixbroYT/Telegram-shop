# Telgram shop backend

Backend of a Telegram store with a database based on **Postgres** in Python using **FastAPI**

---

## ⚙️ Features

- 🧩Ability to add and delete products in the database using commands in the bot.
- 💳Added payment via **Stripe**
- 🛠Easy setup and launch

---

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/FixbroYT/Telegram-shop/tree/master
   cd Telegram-shop

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your API keys:

   ```
   TELEGRAM_TOKEN=your_telegram_bot_token
   DATABASE_URL=your_db_url
   ADMIN_USERNAME=your_tg_username
   STRIPE_APIKEY=your_stripe_secret_key
   FRONTEND_URL=https://your_frontend_url/
   ```

---

## 🛠 Tech Stack

* Python + FastAPI
* SQLAlchemy
* PostgreSQL
* Stripe
* Logging system

---

## 📄 License

MIT License — free to use and modify.
