# Преобразование текстового файла книги в словарь

import os
import sys

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

# Функция, возвращающая строку с текстом страницы и её размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    symbols = [',', '.', '!', ':', ';', '?']
    end = start + size

    if end >= len(text):
        end = len(text)

    while True:
        condition1 = text[end - 1] in symbols
        condition2 = text[end - 2] not in symbols
        condition3 = (end == len(text)) or (end < len(text) and (text[end] not in symbols))

        if condition1 and condition2 and condition3:
            break
        end -= 1

    page_text = text[start:end]

    return (page_text, len(page_text))

# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    pass

# prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))