from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

router = Router()

@router.message(Command(commands='delmenu'))
async def del_main_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text='Кнопка "Menu" удалена')