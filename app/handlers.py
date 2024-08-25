import asyncio
import os
import time as tim
import logging
from datetime import datetime, time, timedelta, date
import re
from aiogram import Bot
from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import app.database.requests as rq
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

class setCategory(StatesGroup):
    category = State()

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    if ((await rq.get_user_tg_id(message.from_user.id) is not None) and (
            await rq.get_user_chat_id(message.from_user.id) is not None)):
        await message.answer(
            f'Labkeeper готов к работе',
            reply_markup=kb.main_buttuns)
    else:
        await message.answer('Добро пожаловать в Labkeeper. Этот бот поможет вам в хранении и быстрому доступу к лабам или любым другим файлам',
            reply_markup=kb.main_buttuns)
        await rq.set_user(message.from_user.id, message.chat.id)

@router.message(F.text == '📁Файлы')
async def get_files(message: types.Message):
    await message.answer('Выберите, что вы хотите посмотреть', reply_markup=kb.output_type)


@router.message(F.text == '➕Добавить категорию')
async def add_category(message: types.Message, state: FSMContext):
    await message.answer('ВВедите категорию')
    await state.set_state(setCategory.category)

@router.message(setCategory.category)
async def set_category(message: types.Message, state: FSMContext):
    await state.update_data(categoty=message.text)
    await rq.add_category(message.text, message.from_user.id)
    data = await state.get_data()
    await message.answer(
        f'Категория: {data["categoty"]}', reply_markup=kb.edit_button)
    await state.clear()


@router.callback_query(F.data == 'data_is_right')
async def accepst_initials(callback: types.CallbackQuery):
    await callback.message.answer('Категория успешно добавлена',
                                  reply_markup=kb.main_buttuns)
    await callback.answer()


@router.callback_query(F.data == 'editor')
async def edit_personal_data(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(setCategory.category)
    await callback.message.answer('Введите категорию', reply_markup=kb.space)


@router.callback_query(F.data == 'by_catas')
async def show_files(callback: types.CallbackQuery):
    keyboard = await kb.get_catas()
    await callback.message.answer('Какую категорию вы хотите посмотреть?', reply_markup=keyboard)