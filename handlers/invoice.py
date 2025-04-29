from aiogram import Router, F, Bot
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import CURRENCY

invoice_router = Router()


class InvoiceStates(StatesGroup):
    WAITING_AMOUNT = State()


@invoice_router.message(Command("pay"))
async def start_invoice(message: Message, state: FSMContext):
    await message.answer("💰 Введите количество звезд:")
    await state.set_state(InvoiceStates.WAITING_AMOUNT)


@invoice_router.message(InvoiceStates.WAITING_AMOUNT)
async def process_amount(message: Message, state: FSMContext, bot: Bot):

    try:
        stars_amount = int(message.text)
        if stars_amount <= 0:
            await message.answer("⚠️ Введите положительное число!")
            return

        await message.answer_invoice(
            title="Покупка звезд",
            description=f"Приобретение {stars_amount} звезд Telegram",
            payload="stars_payment",
            provider_token='',
            currency=CURRENCY,
            prices=[
                LabeledPrice(
                    label=f"{stars_amount} Stars",
                    amount=stars_amount
                )
            ]
        )
        await state.clear()

    except ValueError:
        await message.answer("❌ Некорректный ввод! Введите целое число:")


@invoice_router.pre_checkout_query()
async def pre_checkout_handler(query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(query.id, ok=True)


@invoice_router.message(F.successful_payment)
async def payment_success(message: Message):
    await message.answer("🎉 Оплата прошла успешно! Спасибо за покупку!", message_effect_id='5104841245755180586')