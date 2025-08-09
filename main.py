import asyncio

import uvicorn
from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.handlers import router
from bot.handlers import rt
from config import BOT_TOKEN, FRONTEND_URL
from database.models import init_db

from logger import logger

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_router(rt)

app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def start_bot():
    logger.info("Starting bot...")
    await init_db()
    await dp.start_polling(bot)

async def start_all():
    bot_task = asyncio.create_task(start_bot())
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    api_task = asyncio.create_task(server.serve())

    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    asyncio.run(start_all())