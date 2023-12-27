from copy import deepcopy

from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandStart
from database.database import user_dict_template, users_db
from filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData, IsPageButtonCallbackData
from keyboards.bookmarks_kb import create_bookmarks_kb, create_edit_kb
from keyboards.pagination_kb import create_pagination_kb
from lexicon.lexicon import LEXICON
from services.file_handling import book

router = Router()

def show_pagination_keyboard(page: int = 1) -> tuple[str]:
    middle_button = f'{page}/{len(book)}'
    if page == 1:
        return (middle_button, 'forward')
    elif page == len(book):
        return ('backward', middle_button)
    else:
        return ('backward', middle_button, 'forward')

# Обрабатывает команду /start и добавляет в базу данных, если пользователя нет
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)

# Обрабатывает команду /help и отправляет сообщение со списком доступных команд
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])

# Обрабатывает команду /beginning и отправляет первую страницу книги с кнопками пагинации
@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            *show_pagination_keyboard(users_db[message.from_user.id]['page'])
        )
    )

# Обрабатывает команду /continue и отправляет страницу, на которой пользователь остановился
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            *show_pagination_keyboard(users_db[message.from_user.id]['page'])
        )
    )

# Обрабатывает команду /bookmarks и отправляет список сохраненных закладок, если они есть
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_kb(
                *users_db[message.from_user.id]['bookmarks']
            )
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])

# Обрабатывает нажатие кнопки "вперёд"/"назад"
@router.callback_query(F.data.in_(['forward', 'backward']))
async def process_change_page_press(callback: CallbackQuery):
    if 1 <= users_db[callback.from_user.id]['page'] <= len(book):
        if callback.data == 'forward':
            users_db[callback.from_user.id]['page'] += 1
        else:
            users_db[callback.from_user.id]['page'] -= 1

        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                *show_pagination_keyboard(users_db[callback.from_user.id]['page'])
            )
        )
    await callback.answer()

# Обрабатывает нажатие на номер страницы
@router.callback_query(IsPageButtonCallbackData())
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']
    )
    await callback.answer('Страница добавлена в закладки')


# Обрабатывает нажатие на закладку
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_kb(
            *show_pagination_keyboard(users_db[callback.from_user.id]['page'])
        )
    )

# Обрабатывает нажатие кнопки "Редактировать"
@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_kb(
            *users_db[callback.from_user.id]['bookmarks']
        )
    )

# Обрабатывает нажатие кнопки "Отменить"
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])

# Обрабатывает нажатие закладки во время удаления закладок
@router.callback_query(IsDelBookmarkCallbackData())
async def process_edit_bookmark_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['edit_bookmarks'],
            reply_markup=create_edit_kb(
                *users_db[callback.from_user.id]['bookmarks']
            )
        )
    else:
        await callback.message.edit_text(LEXICON['no_bookmarks'])

# Обрабатывает команду "delmenu"
@router.message(Command(commands='delmenu'))
async def del_main_menu(message: Message, bot: Bot):
    await bot.delete_my_commands()
    await message.answer(text='Кнопка "Menu" удалена')