import json

import requests
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hlink, hbold
from bs4 import BeautifulSoup

from loader import dp


def get_blush():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.46"
    }
    url = "https://iledebeaute.ru/shop/make-up/tint/blush/tip-all_discount-iz-nap/?sortBy=price_min"
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    item_cards = soup.find_all("div", class_="b-showcase__item")
    items_dict = {}
    for item in item_cards:
        item_link_title = item.find("p", class_="b-showcase__item__link")
        item_shtuka = item_link_title.find("a")
        item_id = item_shtuka.get("data-product-id")
        item_link = f'https://iledebeaute.ru{item_shtuka.get("href")}'
        items = item_link_title.find("a").text.strip()
        item_price = item.find("p", class_="b-showcase__item__price")
        item_price_new = item_price.find("span", class_="new")
        item_price_old = item_price.find("span", class_="old")
        item_price_new = str(item_price_new)
        item_price_new = item_price_new[:-8]
        item_price_new = item_price_new[18:]
        item_price_old = str(item_price_old)
        item_price_old = item_price_old[:-8]
        item_price_old = item_price_old[18:]
        item_price_new_num = item_price_new[:-4]
        item_price_new_num = item_price_new_num.replace(" ", "")
        item_price_old_num = item_price_old[:-4]
        item_price_old_num = item_price_old_num.replace(" ", "")
        if item_price_new_num.isnumeric() and item_price_new_num.isnumeric():
            item_price_new_num = int(item_price_new_num)
            item_price_old_num = int(item_price_old_num)
            item_price_profit = item_price_old_num - item_price_new_num
            item_price_discount = 100 - ((item_price_new_num/item_price_old_num)*100)
            item_price_discount = round(item_price_discount)
            items_dict[item_id] = {
                "item_name": items,
                "item_price_new": item_price_new,
                "item_price_old": item_price_old,
                "item_url": item_link,
                "item_price_profit": item_price_profit,
                "item_price_discount": item_price_discount
            }
            print(f"{item_id} | {item_link} | {items} | {item_price_new} | {item_price_old} | {item_price_discount} | {item_price_profit} | {item_price_discount}")

    with open("D:/myPythonProjs/mytgbot/items_dict.json", "w", encoding="utf-8") as file:
        json.dump(items_dict, file, indent=4, ensure_ascii=False)

    return items_dict


@dp.message_handler(Command("ildebote"))
async def discount_sneakers(message: types.Message):
    start_buttons = ["Свекольники", "Тушь", "Помажа"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Товары со скидкой", reply_markup=keyboard)


@dp.message_handler(Text(equals="Свекольники"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Пожалуйста подождите...", reply_markup=ReplyKeyboardRemove())

    get_blush()

    with open("D:/myPythonProjs/mytgbot/items_dict.json", encoding="utf-8") as file:
        blush_dict = json.load(file)

    for k, v in sorted(blush_dict.items()):
        blush = f"{hlink(v['item_name'], v['item_url'])}\n" \
                f"{hbold('Прайс: ')} {v['item_price_old']}\n" \
                f"{hbold('Выгода: ')} {v['item_price_profit']} руб\n" \
                f"{hbold('Прайс со скидкой ')}-{v['item_price_discount']}%: {v['item_price_new']}🔥\n"

        await message.answer(blush, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True)
