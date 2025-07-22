from datetime import datetime, date
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession


import redis
r = redis.Redis()

from model.gemini_model import model
from database.orm_query import orm_get_user
 

gemini = Router()


class Prompt(StatesGroup):
    prompt = State()


@gemini.message(Command('prompt'))
async def post_prompt(message: Message, state: FSMContext, session: AsyncSession):
    await message.answer('<b>Проверка вашей подписки:</b>⏲️')
    try:
        user = await orm_get_user(session, message.from_user.id)
        data_start = user.data_buy
        data_end = user.data_end
        today = date.today()

        if data_start <= today <= data_end:
            await state.set_state(Prompt.prompt)
            await message.answer(f'Ваша подписка действительна✔️\nДата окончания: <b>{data_end}</b>')
            await message.answer(f'Введите ваш запрос:')
        else:
            await state.clear()
            await message.answer('У вас нет действующей подписки❌\nИспользуйте команду /donate')
    except:
        await state.clear()
        await message.answer('Вы еще не разу не приобретали подписку❌\nИспользуйте команду /donate')


@gemini.message(Prompt.prompt, F.text)
async def prompt(message: Message, state: FSMContext):
    prompt = message.text
    user_key = f'user:{message.from_user.id}'
    model_key = f'model:{message.from_user.id}'

    # Добавляем историю, если есть
    if r.llen(user_key) > 0:
        last_prompts = str([x.decode('utf-8') for x in r.lrange(user_key, 0, 2)])  # Берём только 3 последних
        last_answers = str([x.decode('utf-8') for x in r.lrange(model_key, 0, 2)])
        prompt += last_prompts + last_answers

    try:
        with r.pipeline() as pipe:
            pipe.rpush(user_key, prompt)
            pipe.expire(user_key, 100)
            response = model.generate_content(prompt)
            pipe.rpush(model_key, response.text)
            pipe.expire(model_key, 100)
            pipe.execute()

        await message.answer(response.text)
    except Exception as e:
        await message.answer(f'Ошибка: {e}')
        r.delete(user_key, model_key)