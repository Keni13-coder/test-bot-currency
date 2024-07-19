import asyncio
import json
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart


from storage.redis_storage import ABCStorage
from filters.filter_convert import CheckForСurrency
from .utils import foramter_for_message

start_router = Router(name=__name__)


@start_router.message(CommandStart())
async def start(message: Message):
    welcome_message = (
        "<b>Привет!</b> 👋 Добро пожаловать в полезный бот.\n\n"
        "Вот несколько полезных команд, которые вы можете использовать:\n"
        "<b>/exchange currency RUB nominal </b> - <i> Получить стоимость валюты в RUB для кол-во </i>\n"
        "<b>/rates</b> - <i>Получить информацию об актуальных курсах валют в RUB</i>\n"
    )
    await message.answer(welcome_message)

@start_router.message(Command('exchange'), CheckForСurrency())
async def exchange(message: Message, command: CommandObject, storage: ABCStorage):
    currency, _, nominal = command.args.strip().split()
    if result := await storage.fetch_one(currency.upper()):
        await message.answer(
            next(
                f"<b>Дата сбора данных:</b> {result[0]}\n\n<pre>{nominal} {currency} -> {message:.2f} RUB</pre>"
                for message in foramter_for_message(result, currency, nominal)
            )
        )
        
@start_router.message(Command('rates'))
async def rates(message: Message, storage: ABCStorage):
    if results := await storage.fetch_all():
        date_of_collection = results[0][0]
        for data in foramter_for_message(results):
            await message.answer(f"<b>Дата сбора данных:</b> {date_of_collection}\n<pre>{''.join(data)}</pre>")
            
   
@start_router.message()
async def missing_message(message: Message):
    await message.answer('Такой команы нет, попробуйте вызвать\n\exchange\n\\rates')