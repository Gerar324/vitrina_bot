import logging
from aiogram import Bot, Dispatcher

from handlers.invoice import invoice_router


async def main():
    from config import BOT_TOKEN
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(invoice_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import asyncio

    asyncio.run(main())