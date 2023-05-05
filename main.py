import asyncio
from AgendaBot.GabyT import bot1_main
from MenuBot.GabyMenu import bot2_main

async def main():
    await asyncio.gather(
        bot1_main(),
        bot2_main()
    )

if __name__ == "__main__":
    asyncio.run(main())

