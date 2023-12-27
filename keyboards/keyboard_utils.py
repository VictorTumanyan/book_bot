from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_INLINE_BUTTONS

def create_inline_kb(width: int,
                     *args: str,
                     last_button: str | None = None,
                     **kwargs: str) -> InlineKeyboardMarkup:

    # Инициализирум билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_INLINE_BUTTONS[button] if button in LEXICON_INLINE_BUTTONS else button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data= button
            ))

    # Распаковываем список с кнопками в билдер
    kb_builder.row(*buttons, width)
    # Добавляем в билдер последнюю кнопку
    if last_button:
        kb_builder.row(InlineKeyboardButton(
            text=last_button,
            callback_data='last_button'
        ))

    return kb_builder.as_markup()