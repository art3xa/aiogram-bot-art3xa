import json
import requests
from aiogram import types
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hlink

from loader import dp

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "bx-ajax": "true"
}


def get_page(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("index.html", "w") as file:
        file.write(response.text)


def get_json(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("result.json", "w") as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)


def collect_data():
    s = requests.Session()
    response = s.get(
        url="https://salomon.ru/catalog/muzhchiny/obuv/filter/available-is-y/size-is-10.5%20uk/apply/?PAGEN_1=1",
        headers=headers)

    data = response.json()
    pagination_count = data.get("pagination").get("pageCount")

    result_data = []
    items_urls = []
    for page_count in range(1, pagination_count + 1):
        url = f"https://salomon.ru/catalog/muzhchiny/obuv/filter/available-is-y/size-is-10.5%20uk/apply/?PAGEN_1={page_count}"
        r = s.get(url=url, headers=headers)

        data = r.json()
        products = data.get("products")

        for product in products:
            product_colors = product.get("colors")

            for pc in product_colors:
                discount_percent = pc.get("price").get("discountPercent")

                if discount_percent != 0 and pc.get("link") not in items_urls:
                    items_urls.append(pc.get("link"))
                    result_data.append(
                        {
                            "title": pc.get("title"),
                            "category": pc.get("category"),
                            "link": f'https://salomon.ru{pc.get("link")}',
                            "price_base": pc.get("price").get("base"),
                            "price_sale": pc.get("price").get("sale"),
                            "discount_percent": discount_percent
                        }
                    )

        print(f"{page_count}/{pagination_count}")
    with open("result_data.json", "w") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


@dp.message_handler(Command("discounts"))
async def discount_sneakers(message: types.Message):
    start_buttons = ["Кроссовки", "Видеокарты", "Гречка"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Товары со скидкой", reply_markup=keyboard)


@dp.message_handler(Text(equals="Кроссовки"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Please wait...", reply_markup=ReplyKeyboardRemove())

    collect_data()

    with open("result_data.json") as file:
        data = json.load(file)

    for item in data:
        card = f"{hlink(item.get('title'), item.get('link'))}\n" \
               f"{hbold('Категория: ')} {item.get('category')}\n" \
               f"{hbold('Прайс: ')} {item.get('price_base')}\n" \
               f"{hbold('Прайс со скидкой: ')} -{item.get('discount_percent')}%: {item.get('price_sale')}🔥"

        await message.answer(card)
