import re
import json
import uuid 
import requests
import logging
import urllib.parse

from bs4 import BeautifulSoup
from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)

from .utils import OFFSET_PID
from test_tele.config_bot import BOT_CONFIG


async def image_keyboard(query: str, file_name: str) -> InlineKeyboardMarkup:
    buttons = [[
                InlineKeyboardButton("💾" ,
                                     callback_data=f"vip2d {file_name}"),
                InlineKeyboardButton("🔄",
                                     switch_inline_query_current_chat=query),
            ]]
    return InlineKeyboardMarkup(buttons)


async def get_child_page(url: str, limit: int, pid: int, imgs: list, starts: int = 0):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        div_posts = soup.find_all('div', class_='img-box')

        for div_post in div_posts[starts:]:
            div_img = div_post.find('div', class_='main-img')
            img_tag = div_img.find('img')  # Mengakses tag <img> di dalam <div class="main-img">
            if img_tag:  # Memastikan tag <img> ditemukan sebelum mencoba mengakses atribut src
                imgs.append(img_tag.get('src'))
            
            if len(imgs) == limit:
                break
    
    return imgs


async def get_main_page(base_url: str, pid: int, limit: int=OFFSET_PID):
    page_number = pid // 300 + 1
    n = pid % 300 
    post_number = n // 30 + 1
    img_urls = []
    post_dict = {}
    posts = []
    n_loop = 0

    is_first = True

    while len(img_urls) < limit:
        if n_loop >= 5 and len(img_urls) == 0:
            break

        n_loop += 1
        url = f'{base_url}/page/{page_number}' if page_number > 1 else base_url
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            div_posts = soup.find_all('div', class_='post')
            for div_post in div_posts[post_number:]:
                h2_title = div_post.find('h2', class_='entry-title')
                if h2_title: 
                    div_link = div_post.find('div', class_='more-link')
                    url = div_link.find('a').get('href')
                    post_number = 30 % abs(30 - pid) if is_first else 0
                    img_urls = await get_child_page(url, limit, pid, img_urls, post_number)
                    is_first = False
                    
                    div_tag = div_post.find('div', class_='cat-tag')
                    post_dict['main_tag'] = div_tag.find('a').text

                if len(img_urls) >= limit:
                    break

            if len(img_urls) >= limit:
                break

            page_number += 1
            post_number = 1
    
    post_dict['img_urls'] = img_urls
    posts.append(post_dict)
    return posts


async def set_url(query: str) -> str:
    query = query.lower().replace(".2d", "").strip()

    all_tags = {key.lower(): value for key, value in BOT_CONFIG.all_tags.tags.items()}

    input = query.split()
    for tag in input:
        if tag in all_tags:
            query = query.replace(tag, all_tags[tag])
    
    if query == '':
        query = 'おっぱい・乳首'

    tags = urllib.parse.quote(query.strip())
    logging.warning(f"ini tags : {tags}")

    return f"https://vanilla-rock.com/?s={tags}&submit=検索"


async def inline_vanillarock(client, inline_query):
    """Show Vanilla-rock arts"""
    query = inline_query.query

    if not query:
        return

    offset = inline_query.offset
    pid = int(offset) if offset else 0

    url = await set_url(query)

    logging.warning(f"{url}, {pid}, {offset}")

    lists = await get_main_page(url, pid)
    
    if pid == 0 and not lists:
        err_result = [
            InlineQueryResultArticle(
                'No results found', InputTextMessageContent(message_text='No results found.'), 
                id='noresults', description='Please try again with different tags.')
        ]
        await client.answer_inline_query(
            inline_query.id,
            results=err_result
        )
        return

    results = []

    if lists:
        try:
            for url in lists[-1]['img_urls']:
                file_name = url.split("uploads/")[1]
                result = InlineQueryResultPhoto(
                    photo_url=url,
                    id=str(uuid.uuid4()),
                    caption=(
                        f"Main tag : `{lists[-1]['main_tag']}`"
                    ),
                    reply_markup=await image_keyboard(query, file_name),
                )

                results.append(result)
    
            await client.answer_inline_query(
                inline_query.id,
                results=results,
                cache_time=0,
                is_gallery=True,
                next_offset=str(pid + OFFSET_PID)
            )
        except Exception as err:
            logging.error(err)


async def get_vr_file(url):
    return f"https://vanilla-rock.com/wp-content/uploads/{url}"


