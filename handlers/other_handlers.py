from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

router = Router()

@router.message()
async def send_echo(message: Message):
    await message.answer(f'Я не знаю как реагировать на: {message.text}')