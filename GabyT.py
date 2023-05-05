from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import json

TOKEN = '5799434637:AAEeUVstwBaH02-Vv2J5O5uMSpaUHhkmBfQ'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola, ¿en qué puedo ayudarte?")

def set_task(update, context):
    # Obtener la tarea y la fecha del mensaje del usuario
    message = update.message.text
    task, date = message.split(" ", 1)

    # Convertir la fecha en un objeto datetime
    date = datetime.datetime.strptime(date, '%d/%m/%Y').date()

    # Obtener la lista de tareas existentes para esta fecha
    task_list = context.user_data.get(str(date), [])

    # Agregar la nueva tarea a la lista
    task_list.append(task)

    # Actualizar el diccionario de tareas del usuario
    context.user_data[str(date)] = task_list

    # Confirmar la creación de la tarea
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Tarea '{task}' creada para el {date}.")

def show_tasks(update, context):
    # Obtener el diccionario de tareas del usuario
    task_dict = context.user_data

    # Convertir el diccionario en una cadena JSON
    task_json = json.dumps(task_dict, indent=4)

    # Enviar la cadena JSON como un mensaje al usuario
    context.bot.send_message(chat_id=update.effective_chat.id, text=task_json)    

def get_tasks(update, context):
    # Obtener la fecha del mensaje del usuario
    date_str = update.message.text

    # Convertir la fecha en un objeto datetime
    date = datetime.datetime.strptime(date_str, '%d/%m/%Y').date()

    # Obtener la lista de tareas existentes para esta fecha
    task_list = context.user_data.get(str(date), [])

    # Si no hay tareas para esta fecha, mostrar un mensaje al usuario
    if not task_list:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"No hay tareas para el {date}.")
    # Si hay tareas para esta fecha, mostrar la lista de tareas al usuario
    else:
        task_str = "\n".join([f"- {task}" for task in task_list])
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Tareas para el {date}:\n{task_str}")

def main():
    # Crear un objeto de actualización y un objeto de despachador
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Agregar manejadores de comandos y mensajes
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^\w+ \d{1,2}/\d{1,2}/\d{4}$'), set_task))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^\d{1,2}/\d{1,2}/\d{4}$'), get_tasks))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()