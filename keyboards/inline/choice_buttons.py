from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import URL_APPLES, URL_PEARS
from keyboards.inline.callback_datas import buy_callback

choice_items = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Купить яблоки", callback_data=buy_callback.new(
                item_name="apple", quantity=2
            )),
            InlineKeyboardButton(text="Купить груши", callback_data="buy:pear:5"),
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ]
)

pears_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Купи тут", url=URL_PEARS)
        ]
    ]
)

apples_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Купи тут", url=URL_APPLES)
        ]
    ]
)