import telegram
import datetime
from pytz import timezone
import asyncio

bot = telegram.Bot(token='5799434637:AAEeUVstwBaH02-Vv2J5O5uMSpaUHhkmBfQ')

async def enviar_mensaje(texto):
    await bot.send_message(chat_id='CHAT_ID', text=texto)

async def main():
    while True:
        ahora = datetime.datetime.now(timezone('America/Mexico_City'))
        if ahora.strftime("%Y-%m-%d %H:%M") == "2023-04-27 05:50":
            await enviar_mensaje('Tienes reunión con tu director de TFN.')
        elif ahora.strftime("%Y-%m-%d %H:%M") == "2023-04-27 13:34":
            await enviar_mensaje('Buenos días, termina de llenar la solicitud para consultar los préstamos hipotecarios.')
        elif ahora.strftime("%Y-%m-%d %H:%M") == "2023-04-27 08:10":
            await enviar_mensaje('Envía los correos para los documentos de UPIITA.')
        elif ahora.hour == 18 and ahora.minute == 0:
            await enviar_mensaje('¡Ya es hora de terminar el trabajo! Descansa y diviértete.')
        await asyncio.sleep(60)  # Esperar un minuto antes de revisar la hora nuevamente

if __name__ == '__main__':
    asyncio.run(main())

