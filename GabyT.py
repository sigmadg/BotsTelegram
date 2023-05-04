import logging
from datetime import date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Configurar el registro de eventos (logging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Colocar aquí tu token de API de Telegram
API_TOKEN = "5799434637:AAEeUVstwBaH02-Vv2J5O5uMSpaUHhkmBfQ"

# Estructura de datos para almacenar eventos recurrentes y actividades pendientes
eventos_recurrentes = {}
actividades_pendientes = []

def start(update: Update, context: CallbackContext):
    update.message.reply_text("¡Hola! Soy tu agenda para eventos recurrentes y actividades pendientes.")

def agregar_evento_recurrente(update: Update, context: CallbackContext):
    try:
        dia = context.args[0].lower()
        evento = ' '.join(context.args[1:])
        
        if dia not in eventos_recurrentes:
            eventos_recurrentes[dia] = []
        eventos_recurrentes[dia].append(evento)
        
        update.message.reply_text(f"Evento '{evento}' agregado al día {dia}.")
    except (IndexError, ValueError):
        update.message.reply_text("Uso: /agregar_evento_recurrente <día> <evento>")

def ver_eventos_recurrentes(update: Update, context: CallbackContext):
    dia = date.today().strftime('%A').lower()
    
    if dia in eventos_recurrentes and eventos_recurrentes[dia]:
        eventos_hoy = "\n".join(eventos_recurrentes[dia])
        update.message.reply_text(f"Eventos recurrentes para hoy:\n{eventos_hoy}")
    else:
        update.message.reply_text("No hay eventos recurrentes para hoy.")

def agregar_actividad_pendiente(update: Update, context: CallbackContext):
    actividad = ' '.join(context.args)
    actividades_pendientes.append(actividad)
    update.message.reply_text(f"Actividad '{actividad}' agregada a la lista de pendientes.")

def ver_actividades_pendientes(update: Update, context: CallbackContext):
    if actividades_pendientes:
        lista_pendientes = "\n".join(actividades_pendientes)
        update.message.reply_text(f"Lista de actividades pendientes:\n{lista_pendientes}")
    else:
        update.message.reply_text("No hay actividades pendientes.")

def main():
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("agregar_evento_recurrente", agregar_evento_recurrente))
    dispatcher.add_handler(CommandHandler("ver_eventos_recurrentes", ver_eventos_recurrentes))
    dispatcher.add_handler(CommandHandler("agregar_actividad_pendiente", agregar_actividad_pendiente))
    dispatcher.add_handler(CommandHandler("ver_actividades_pendientes", ver_actividades_pendientes))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
