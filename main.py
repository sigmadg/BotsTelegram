import asyncio
from AgendaBot.GabyT import bot1_main
from MenuBot.GabyMenu import bot2_main

async def main():
    tasks = [bot1_main(), bot2_main()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
