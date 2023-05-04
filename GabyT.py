import logging
from datetime import datetime
from telegram.ext import Updater, CommandHandler, CallbackContext

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

API_TOKEN = "5799434637:AAEeUVstwBaH02-Vv2J5O5uMSpaUHhkmBfQ"

eventos_recurrentes = {}
actividades_pendientes = []

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy tu agenda para eventos recurrentes y actividades pendientes.")

def agregar_evento_recurrente(update, context):
    try:
        dia = context.args[0].lower()
        evento = ' '.join(context.args[1:])
        
        if dia not in eventos_recurrentes:
            eventos_recurrentes[dia] = []
        eventos_recurrentes[dia].append(evento)
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Evento '{evento}' agregado al día {dia}.")
    except (IndexError, ValueError):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Uso: /agregar_evento_recurrente <día> <evento>")

def ver_eventos_recurrentes(update, context):
    dia = datetime.today().strftime('%A').lower()
    
    if dia in eventos_recurrentes and eventos_recurrentes[dia]:
        eventos_hoy = "\n".join(eventos_recurrentes[dia])
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Eventos recurrentes para hoy:\n{eventos_hoy}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No hay eventos recurrentes para hoy.")

def agregar_actividad_pendiente(update, context):
    actividad = ' '.join(context.args)
    actividades_pendientes.append(actividad)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Actividad '{actividad}' agregada a la lista de pendientes.")

def ver_actividades_pendientes(update, context):
    if actividades_pendientes:
        lista_pendientes = "\n".join(actividades_pendientes)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Lista de actividades pendientes:\n{lista_pendientes}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No hay actividades pendientes.")

def main():
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("agregar_evento_recurrente", agregar_evento_recurrente, pass_args=True))
    dispatcher.add_handler(CommandHandler("ver_eventos_recurrentes", ver_eventos_recurrentes))
    dispatcher.add_handler(CommandHandler("agregar_actividad_pendiente", agregar_actividad_pendiente, pass_args=True))
    dispatcher.add_handler(CommandHandler("ver_actividades_pendientes", ver_actividades_pendientes))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

