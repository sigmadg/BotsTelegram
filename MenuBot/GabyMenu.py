import datetime
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

TOKEN_MENU = "6039729307:AAEvZj0GHeRzyK9QMCtNU7IRLR-Cn_vZzTA"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_MENU)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

orders = {}

async def start(message: types.Message):
    keyboard = [
        [
            InlineKeyboardButton("Cuernito - $25", callback_data="Cuernito"),
            InlineKeyboardButton("Molletes - $35", callback_data="Molletes"),
        ],
        [
            InlineKeyboardButton("Chilaquiles Pollo - $40", callback_data="Chilaquiles_Pollo"),
            InlineKeyboardButton("Chilaquiles Manchego - $45", callback_data="Chilaquiles_Manchego"),
        ],
        [
            InlineKeyboardButton("Huevos Jamón - $35", callback_data="Huevos_Jamon"),
            InlineKeyboardButton("Huevos Mexicana - $35", callback_data="Huevos_Mexicana"),
        ],
        [
            InlineKeyboardButton("Huevos Salchichas - $35", callback_data="Huevos_Salchichas"),
        ],
        [
            InlineKeyboardButton("Torta Pechuga - $25", callback_data="Torta_Pechuga"),
            InlineKeyboardButton("Torta Salchicha - $25", callback_data="Torta_Salchicha"),
        ],
        [
            InlineKeyboardButton("Torta Huevo y Jamón - $25", callback_data="Torta_Huevos_Jamon"),
            InlineKeyboardButton("Torta Huevo y Salchicha - $25", callback_data="Torta_Huevos_Salchicha"),
        ],
        [
            InlineKeyboardButton("Torta Pierna - $25", callback_data="Torta_Pierna"),
            InlineKeyboardButton("Torta Chilaquiles - $25", callback_data="Torta_Chilaquiles"),
        ],
        [
            InlineKeyboardButton("Café - $15", callback_data="Cafe"),
            InlineKeyboardButton("Fruta - $25", callback_data="Fruta"),
        ],
        [
            InlineKeyboardButton("Agua de Litro - $25", callback_data="Agua_Litro"),
            InlineKeyboardButton("Agua de Medio - $15", callback_data="Agua_Medio"),
        ],
        [
            InlineKeyboardButton("Panquesitos Queso - $25", callback_data="Panquesitos_Queso"),
            InlineKeyboardButton("Panquesitos Oreo - $25", callback_data="Panquesitos_Oreo"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(row_width=2)
    for row in keyboard:
        reply_markup.add(*row)

    await message.reply("Por favor selecciona una opción:", reply_markup=reply_markup)


async def button_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    item = callback_query.data
    if user_id not in orders:
        orders[user_id] = {
            "Cuernito": 0,
            "Molletes": 0,
            "Chilaquiles_Pollo": 0,
            "Chilaquiles_Manchego": 0,
            "Huevos_Jamon": 0,
            "Huevos_Salchichas": 0,
            "Huevos_Mexicana": 0,
            "Torta_Pechuga": 0,
            "Torta_Chilaquiles": 0,
            "Torta_Salchicha": 0,
            "Torta_Huevos_Jamon": 0,
            "Torta_Huevos_Salchicha": 0,
            "Torta_Pierna": 0,
            "Cafe": 0,
            "Fruta": 0,
            "Agua_Litro": 0,
            "Agua_Medio": 0,
            "Panquesitos_Queso": 0,
            "Panquesitos_Oreo": 0,
        }

    orders[user_id][item] += 1
    await callback_query.answer(f"Agregaste 1 {item}")


def order_summary():
    summary = ""
    total = 0
    for user_id, order in orders.items():
        user_total = 0
        user_order = ""
        for item, quantity in order.items():
            if quantity > 0:
                if item == "Cuernito":
                    price = 25
                elif item == "Molletes":
                    price = 35
                elif item == "Chilaquiles_Pollo":
                    price = 40
                elif item == "Chilaquiles_Manchego":
                    price = 45
                elif item == "Huevos_Jamon":
                    price = 35
                elif item == "Huevos_Salchichas":
                    price = 35
                elif item == "Huevos_Mexicana":
                    price = 35
                elif item == "Torta_Pechuga":
                    price = 25
                elif item == "Torta_Chilaquiles":
                    price = 25
                elif item == "Torta_Salchicha":
                    price = 25
                elif item == "Torta_Huevos_Jamon":
                    price = 25
                elif item == "Torta_Huevos_Salchicha":
                    price = 25
                elif item == "Torta_Pierna":
                    price = 25
                elif item == "Cafe":
                    price = 15
                elif item == "Fruta":
                    price = 25
                elif item == "Agua_Litro":
                    price = 25
                elif item == "Agua_Medio":
                    price = 15
                elif item == "Panquesitos_Queso":
                    price = 25
                elif item == "Panquesitos_Oreo":
                    price = 25
                user_order += f"{quantity} {item} - ${price * quantity}\n"
                user_total += price * quantity
        if user_order:
            summary += f"Usuario {user_id}:\n{user_order}Total: ${user_total}\n\n"
            total += user_total
    if not summary:
        summary = "No hay pedidos."
    else:
        summary += f"Total general: ${total}"
    return summary


async def summary(message: types.Message):
    current_time = datetime.datetime.now().time()
    if current_time >= datetime.time(8, 50):
        await message.reply(order_summary())
    else:
        await message.reply("La lista de pedidos se mostrará a las 8:50 AM.")


async def on_startup(dp):
    await bot.send_message(chat_id="@DesayunoGSBot", text="Bot has been started")


async def on_shutdown(dp):
    await bot.send_message(chat_id="@DesayunoGSBot", text="Bot has been stopped")

async def bot2_main():
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(summary, commands=["summary"])
    dp.register_callback_query_handler(button_callback)

    await dp.start_polling(on_startup=on_startup, on_shutdown=on_shutdown)
