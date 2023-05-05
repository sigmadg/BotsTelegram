import datetime
import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

TOKEN = '5799434637:AAEeUVstwBaH02-Vv2J5O5uMSpaUHhkmBfQ'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def on_start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Hola, ¿en qué puedo ayudarte?")

async def set_task(message: types.Message):
    # Obtener la tarea y la fecha del mensaje del usuario
    text = message.text
    task, date = text.split(" ", 1)

    # Convertir la fecha en un objeto datetime
    date = datetime.datetime.strptime(date, '%d/%m/%Y').date()

    # Crear user_data en caso de que no exista
    if not hasattr(message, "user_data"):
        message.user_data = {}

    # Obtener la lista de tareas existentes para esta fecha
    task_list = message.user_data.get(str(date), [])

    # Agregar la nueva tarea a la lista
    task_list.append(task)

    # Actualizar el diccionario de tareas del usuario
    message.user_data[str(date)] = task_list

    # Confirmar la creación de la tarea
    await bot.send_message(chat_id=message.chat.id, text=f"Tarea '{task}' creada para el {date}.")

async def show_tasks(message: types.Message):
    # Crear user_data en caso de que no exista
    if not hasattr(message, "user_data"):
        message.user_data = {}

    # Obtener el diccionario de tareas del usuario
    task_dict = message.user_data

    # Convertir el diccionario en una cadena JSON
    task_json = json.dumps(task_dict, indent=4)

    # Enviar la cadena JSON como un mensaje al usuario
    await bot.send_message(chat_id=message.chat.id, text=task_json)

async def get_tasks(message: types.Message):
    # Crear user_data en caso de que no exista
    if not hasattr(message, "user_data"):
        message.user_data = {}

    # Obtener la fecha del mensaje del usuario
    date_str = message.text

    # Convertir la fecha en un objeto datetime
    date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()

    # Obtener la lista de tareas existentes para esta fecha
    task_list = message.user_data.get(str(date), [])

    # Si no hay tareas para esta fecha, mostrar un mensaje al usuario
    if not task_list:
        await bot.send_message(chat_id=message.chat.id, text=f"No hay tareas para el {date}.")
    # Si hay tareas para esta fecha, mostrar la lista de tareas al usuario
    else:
        task_str = "\n".join([f"- {task}" for task in task_list])
        await bot.send_message(chat_id=message.chat.id, text=f"Tareas para el {date}:\n{task_str}")

async def send_daily_agenda(user_data):
    # Obtener la fecha actual
    today = datetime.date.today()

    # Obtener la lista de tareas para hoy
    task_list = user_data.get(str(today), [])

    # Si hay tareas para hoy, enviar un mensaje con la lista de tareas a las 6 am
    if task_list:
        task_str = "\n".join([f"- {task}" for task in task_list])
        await bot.send_message(chat_id='5799434637:AAEeUVstwBaH02-Vv2J5O5uMSpaUHhkmBfQ', text=f"Tareas para el {today}:\n{task_str}")
    else:
        await bot.send_message(chat_id='5799434637:AAEeUVstwBaH02-Vv2J5O5uMSpaUHhkmBfQ', text=f"No hay tareas para el {today}.")

async def bot1_main():
    from aiogram.dispatcher.filters import Command, Text

    # Reemplaza los MessageHandler y CommandHandler con los filtros de aiogram
    dp.register_message_handler(on_start, Command("start"))
    dp.register_message_handler(set_task, regexp=r'^\w+ \d{1,2}/\d{1,2}/\d{4}$')
    dp.register_message_handler(get_tasks, regexp=r'^\d{1,2}/\d{1,2}/\d{4}$')

    # Iniciar el bot
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(bot1_main())

    