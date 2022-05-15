import json
from datetime import datetime

import requests
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hbold, hlink
from bs4 import BeautifulSoup

from loader import dp


def get_hltvnews():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.46"
    }

    url = "https://www.hltv.org"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("a", class_="newsline")
    hltvnews_dict = {}
    for article in articles_cards:
        article_text = article.find("div", class_="newstext").text.strip()
        article_recent = article.find("div", class_="newsrecent").text.strip()
        article_url = f'https://www.hltv.org{article.get("href")}'
        article_id = article_url.split("/")[-2]

        print(f"{article_text} | {article_recent} | {article_url} | {article_id}")
        hltvnews_dict[article_id] = {
            "article_text": article_text,
            "article_recent": article_recent,
            "article_url": article_url
        }

    with open("D:/myPythonProjs/mytgbot/hltvnews_dict.json", "w") as file:
        json.dump(hltvnews_dict, file, indent=4, ensure_ascii=False)

    return hltvnews_dict


def check_new_hltvnews():
    with open("D:/myPythonProjs/mytgbot/hltvnews_dict.json") as file:
        hltvnews_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.46"
    }

    url = "https://www.hltv.org"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("a", class_="newsline")

    fresh_htlvnews = {}
    for article in articles_cards:
        article_url = f'https://www.hltv.org{article.get("href")}'
        article_id = article_url.split("/")[-2]

        if article_id in hltvnews_dict:
            continue
        else:
            article_text = article.find("div", class_="newstext").text.strip()
            article_recent = article.find("div", class_="newsrecent").text.strip()

            hltvnews_dict[article_id] = {
                "article_text": article_text,
                "article_recent": article_recent,
                "article_url": article_url
            }

            fresh_htlvnews[article_id] = {
                "article_text": article_text,
                "article_recent": article_recent,
                "article_url": article_url
            }

    with open("D:/myPythonProjs/mytgbot/hltvnews_dict.json", "w") as file:
        json.dump(hltvnews_dict, file, indent=4, ensure_ascii=False)

    return fresh_htlvnews


@dp.message_handler(commands="hltvnews")
async def news(message: types.Message):
    start_buttons = ["Все новости HLTV", "Последние 5 новостей HLTV", "Свежие новости HLTV"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Лента новостей", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости HLTV"))
async def get_all_news(message: types.Message):
    # with open("D:/myPythonProjs/mytgbot/hltvnews_dict.json") as file:
    #     hltvnews_dict = json.load(file)
    hltvnews_dict = get_hltvnews()
    for k, v in sorted(hltvnews_dict.items()):
        # news = f"<b>{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}</b>\n" \
        #        f"<u>{v['article_title']}</u>\n" \
        #        f"<code>{v['article_desc']}</code>\n" \
        #        f"{v['article_url']}"
        # news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
        #        f"{hunderline(v['article_title'])}\n" \
        #        f"{hcode(v['article_desc'])}\n" \
        #        f"{hlink(v['article_title'], v['article_url'])}"
        hltvnews = f"{hbold(v['article_recent'])}\n" \
                   f"{hlink(v['article_text'], v['article_url'])}"

        await message.answer(hltvnews, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Последние 5 новостей HLTV"))
async def get_last_five_news(message: types.Message):
    # with open("D:/myPythonProjs/mytgbot/hltvnews_dict.json") as file:
    #     hltvnews_dict = json.load(file)
    hltvnews_dict = get_hltvnews()
    for k, v in sorted(hltvnews_dict.items())[-5:]:
        hltvnews = f"{hbold(v['article_recent'])}\n" \
                   f"{hlink(v['article_text'], v['article_url'])}"

        await message.answer(hltvnews, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Свежие новости HLTV"))
async def get_fresh_news(message: types.Message):
    fresh_hltvnews = check_new_hltvnews()

    if len(fresh_hltvnews) >= 1:
        for k, v in sorted(fresh_hltvnews.items()):
            hltvnews = f"{hbold(v['article_recent'])}\n" \
                   f"{hlink(v['article_text'], v['article_url'])}"

            await message.answer(hltvnews, reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer("Пока нет свежих новостей...", reply_markup=ReplyKeyboardRemove())
