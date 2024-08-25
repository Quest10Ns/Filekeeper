import os
from app.database.models import async_session
from app.database.models import User, Category
from sqlalchemy import select, update, delete, and_
from datetime import datetime, time, date
import time as tim
import aiofiles
import re


async def set_user(tg_id, chat_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if not user:
            session.add(User(telegram_id=tg_id, telegram_chat_id = chat_id))
            await session.commit()


async def get_user_tg_id(tg_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            return user.telegram_id

async def get_user_chat_id(tg_id):
    async with  async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            return user.telegram_chat_id

async def add_category(category, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).filter(User.telegram_id == tg_id))
        if user:
            cata = await session.scalar(select(Category).filter(and_(Category.category == category, Category.user_id == user.id)))
            if not cata:
                session.add(Category(category = category, user_id = user.id))
                await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))