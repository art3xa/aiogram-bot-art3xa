from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Начать диалог"),
            types.BotCommand("help", "Вывести справку"),
            # types.BotCommand("me", "Узнать инфу о себе"),
            types.BotCommand("news", "Посмотреть новости"),
            types.BotCommand("hltvnews", "Новости HLTV"),
            types.BotCommand("wiki", "Википедия"),
            types.BotCommand("items", "Купить что-то"),
            types.BotCommand("weather", "Узнать погоду"),
            types.BotCommand("discounts", "Скидки на товары"),
            types.BotCommand("ildebote", "Лут из ИЛЬ ДЕ БОТЭ"),
        ]
    )
