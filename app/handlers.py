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
    await message.answer('Выберите, что вы хотите посмотреть', reply_markup='output_type')



