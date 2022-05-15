import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_datas import buy_callback
from keyboards.inline.choice_buttons import choice_items, pears_keyboard, apples_keyboard
from loader import dp


@dp.message_handler(Command("items"))
async def show_items(message: Message):
    await message.answer(text="На продажу есть 2 товара: Яблоки и Груши. \n"
                              "Если вам ничего не нужно - жмите отмену",
                         reply_markup=choice_items)


@dp.callback_query_handler(buy_callback.filter(item_name="apple"))
async def buying_apple(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data=}")
    quantity = callback_data.get("quantity")
    await call.message.answer(f"Вы выбрали яблоки. Яблок всего {quantity}. Спасибо!",
                              reply_markup=apples_keyboard)


@dp.callback_query_handler(buy_callback.filter(item_name="pear"))
async def buying_pear(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data=}")
    quantity = callback_data.get("quantity")
    await call.message.answer(f"Вы выбрали грушу. Груш всего {quantity}. Спасибо!",
                              reply_markup=pears_keyboard)


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    await call.answer("Вы отменили эту покупку!", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None) #изменяет сообщение к которому было прикреплено (убрал клаву)
