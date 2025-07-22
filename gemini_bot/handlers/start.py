from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext # Новый импорт
from aiogram.fsm.state import State, StatesGroup # Новый импорт

start = Router()


@start.message(CommandStart())
async def start_com(message: Message):
    await message.answer('Привет! Я бот, на основе GEMINI, написанный Мишей!')


