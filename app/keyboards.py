from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

from app.database.requests import *

from aiogram.utils.keyboard import InlineKeyboardBuilder

import datetime
space = ReplyKeyboardRemove()

edit_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Подтвердить', callback_data='data_is_right'),
     InlineKeyboardButton(text='✏️Изменить', callback_data='editor')]])

main_buttuns = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='📁Файлы')],
              [KeyboardButton(text='➕Добавить категорию'), KeyboardButton(text='🧷Добавить файл')]], resize_keyboard=True)

output_type = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='По категориям', callback_data='by_catas'),
     InlineKeyboardButton(text='Все файлы', callback_data='all_files')]])

async def get_catas():
    all_cata = await get_categories()
    keyboard = InlineKeyboardBuilder()
    categoties = []
    for category in all_cata:
        if category.category not in categoties:
            categoties.append(category.category)
    for cata in categoties:
        keyboard.add(InlineKeyboardButton(text=f'{cata}', callback_data=f'category_{cata}'))
    return keyboard.as_markup()


async def get_catas_edit():
    all_cata = await get_categories()
    keyboard = InlineKeyboardBuilder()
    categoties = []
    for category in all_cata:
        if category.category not in categoties:
            categoties.append(category.category)
    for cata in categoties:
        keyboard.add(InlineKeyboardButton(text=f'{cata}', callback_data=f'category_edit_{cata}'))
    return keyboard.as_markup()