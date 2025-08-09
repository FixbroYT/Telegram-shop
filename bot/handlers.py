import io
import logging
import os.path
import re

from PIL import Image

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
import requests
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_USERNAME, BOT_TOKEN, FRONTEND_URL
from database.requests import create_product

from database import requests as rq

rt = Router()

URI_INFO = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id="
URI = f"https://api.telegram.org/file/bot{BOT_TOKEN}/"

logger = logging.getLogger(__name__)

class AddProduct(StatesGroup):
    name = State()
    price = State()
    image = State()

@rt.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Hello! Welcome to bot!", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Go shopping!", web_app=WebAppInfo(url=FRONTEND_URL))]
    ]))

@rt.message(Command("add_product"))
async def add_product(message: Message, state: FSMContext):
    if message.from_user.username == ADMIN_USERNAME:
        await state.set_state(AddProduct.name)
        await message.answer("Enter the name of the product")
    else:
        await message.answer("You can't add products!")

@rt.message(AddProduct.name)
async def product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProduct.price)
    await message.answer("Enter the price of the product")

def is_float(string):
  try:
    float(string)
    return True
  except ValueError:
    return False

@rt.message(AddProduct.price)
async def product_price(message: Message, state: FSMContext):
    if is_float(message.text):
        price = float(message.text)
        await state.update_data(price=price)
        await state.set_state(AddProduct.image)
        await message.answer("Upload product image")
    else:
        await message.answer("Incorrect product price, enter the product price, for example: 2.99")

@rt.message(AddProduct.image, F.document)
async def product_image(message: Message, state: FSMContext):
    document = message.document

    if document.mime_type != "image/png":
        await message.answer("Invalid photo type, please upload a png photo")
        return

    response = requests.get(URI_INFO + document.file_id)
    file_path = response.json()["result"]["file_path"]
    img = requests.get(URI + file_path)
    img = Image.open(io.BytesIO(img.content))
    file_name = document.file_name

    img.save(f"{os.path.abspath(__name__)}/../static/images/{file_name}", format="PNG")

    await state.update_data(image=file_name)

    data = await state.get_data()
    await create_product(product_name=data["name"], product_price=data["price"], product_image_url=data["image"])

    await message.answer("Photo has been saved and item has been added!")

@rt.message(Command("delete_product"))
async def delete_product(message: Message):
    if message.from_user.username == ADMIN_USERNAME:
        await message.answer("Choose product:", reply_markup=make_inline_keyboard(await rq.get_all_products()))
    else:
        await message.answer("You can't delete products!")

@rt.callback_query(F.data)
async def delete_product_callback(callback: CallbackQuery):
    callback_product_name = re.sub(r"product_", "", callback.data)
    result = await rq.delete_product(callback_product_name)
    if result:
        await callback.answer(f"You deleted successfully {callback_product_name}")
    else:
        await callback.answer(f"Product {callback_product_name} not found in database")

    products = await rq.get_all_products()
    if products:
        await callback.message.edit_text("Done! Here are the rest of the products:", reply_markup=make_inline_keyboard(products))
    else:
        await callback.message.edit_text("Done! There's no more products left")

def make_inline_keyboard(products):
    keyboard = InlineKeyboardBuilder()
    for product in products:
        keyboard.add(InlineKeyboardButton(text=product["name"].capitalize(), callback_data=f"product_{product["name"]}"))

    return keyboard.adjust(2).as_markup()