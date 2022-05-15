from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Вывести справку",
            "/news - Посмотреть новости",
            "/hltvnews - Новости HLTV",
            "/wiki - Википедия",
            "/items - Купить что-то",
            "/weather - Узнать погоду",
            "/discounts - Скидки на товары",
            "/ildebote - Лут из ИЛЬ ДЕ БОТЭ",
            )
    
    await message.answer("\n".join(text))
