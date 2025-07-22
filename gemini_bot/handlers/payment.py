import os
import uuid
from datetime import datetime, timedelta, date
from asyncio.log import logger
from aiogram import F, Router
from aiogram.types import LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from database.orm_query import orm_get_user


pay = Router()


@pay.message(Command('donate'))
async def top_up(message: Message, session: AsyncSession):
    try:
        user = await orm_get_user(session, message.from_user.id)
        data_start = user.data_buy
        data_end = user.data_end
        today = date.today()
        if data_start <= today <= data_end:
            await message.answer(f'Ваша подписка ещё действительна✔️\nДата окончания: <b>{data_end}</b>')
            return
        else:
            raise(Exception)
    except:
        payload = f"donate-{uuid.uuid4()}"
        await message.bot.send_invoice(
            message.from_user.id,
            title="Подписка на бота",
            description="Активация подписки на бота на 1 месяц",
            provider_token=os.getenv('PAYMENTS_PAYMASTER'),
            currency="rub",
            photo_url="https://avatars.dzeninfra.ru/get-zen_doc/271828/pub_67d95eb5b75bbe115da9b9d9_67d95ebdb75bbe115da9bd9b/scale_1200",
            photo_width=416,
            photo_height=234,
            photo_size=416,
            is_flexible=False,
            prices=[LabeledPrice(label="Подписка на 1 месяц", amount=30000)],
            start_parameter="donate",
            payload=payload,
            need_email=True  # Запросить email
        )


@pay.pre_checkout_query()
async def process_pre_checkout(pre_checkout: PreCheckoutQuery):
    await pre_checkout.answer(ok=True)


@pay.message(F.successful_payment)
async def process_successful_payment(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    payment = message.successful_payment
    payload = payment.invoice_payload
    today = datetime.now().date() 
    subscription_days = 30
    subscription_end = today + timedelta(days=subscription_days)

    user = User(id_user=user_id, payload=payload, data_buy=today, data_end=subscription_end)
    session.add(user)
    
    try:
        await session.commit()
        await message.answer("✅ Оплата прошла успешно! Подписка активирована.")
    except Exception as e:
        await session.rollback()
        await message.answer("❌ Ошибка при сохранении подписки. Попробуйте позже.")
        logger.error(f"Error saving user: {e}")