import re
import json
import uuid 
import shlex
import asyncio
import logging
import urllib.parse

from pyrogram import enums
from pyrogram.types import InputMediaPhoto, InputMediaDocument
from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)

from .utils import OFFSET_PID, IMG_EXT, GIF_EXT, VID_EXT, gallery_dl, get_tags, not_found_msg


async def image_keyboard(query: str, my_list: list[str]) -> InlineKeyboardMarkup:
    url = my_list['img_url'].split("/img/")[-1]
    buttons = [[
                InlineKeyboardButton("👤🔄",
                                     switch_inline_query_current_chat=f".px id:{my_list['artist_id']}"),
                InlineKeyboardButton("🔗🔄",
                                     switch_inline_query_current_chat=f".px {my_list['id']}")
            ],[
                InlineKeyboardButton("💾" ,
                                     callback_data=f"px {url}"),
                InlineKeyboardButton("🔄",
                                     switch_inline_query_current_chat=query),
            ]]
    return InlineKeyboardMarkup(buttons)


async def set_info_dict(gallery_dl_result) -> list[dict]:
    """Set dict based on website"""
    my_dict = {}
    lists: list[my_dict] = []
    
    for elemen in gallery_dl_result:
        if elemen[0] == 3:
            my_dict = {}
            my_dict['img_url'] = elemen[1]
            my_dict['id'] = str(elemen[2]['id'])
            my_dict['artist'] = str(elemen[2]['user']['name']).encode('utf-8').decode('utf-8')
            my_dict['artist_id'] = str(elemen[2]['user']['id'])
            my_dict['tags'] = await get_tags(elemen[2]['tags'])
            my_dict['title'] = str(elemen[2]['title']).encode('utf-8').decode('utf-8')
            my_dict['extension'] = elemen[2]['extension']
            my_dict['thumbnail'] = await get_thumbnail(elemen[1])
            my_dict['sample_img'] = my_dict['thumbnail'].replace("400x400", "600x600")
            lists.append(my_dict)
    return lists


async def set_url(query: str) -> str:
    def_tag = 's_mode=s_tag'
    url = str(query).strip().lower().replace(".px", "").lstrip()

    if str(url).isdigit():
        return f"https://www.pixiv.net/en/artworks/{url}"

    id_pattern = r'(id:)(\w+)'
    id_match = re.search(id_pattern, url)
    if id_match:
        return f"https://www.pixiv.net/en/users/{id_match.group(2)}/artworks"
    
    modes = {
        "-exact": "",
        "-r18": "&mode=r18",
        "-safe": "&mode=safe",
        "-no_ai": "&ai_type=1"
    }

    for mode, val in modes.items():
        if mode in url:
            if mode == '-exact':
                def_tag = ""
            else:
                def_tag += val
            url = url.replace(mode, "")

    # Default = sangonomiya kokomi R18 
    if url == '':
        url = '珊瑚宮心海' 
        def_tag += "&mode=r18"

    return f"https://www.pixiv.net/en/tags/{url}/artworks?{def_tag}"


async def get_thumbnail(image_url: str) -> str:
    # https://i.pximg.net/c/600x600/img-master/img/2023/12/14/00/26/56/114205137_p11_master1200.jpg
    url = image_url.split("/img/")[-1]
    url, ext = url.split(".")
    return f"https://i.pximg.net/c/400x400/img-original/img/{url}.{ext}"


async def inline_pixiv(client, inline_query):
    """Show Pixiv artworks"""
    query = inline_query.query

    if not query:
        return

    offset = inline_query.offset
    pid = int(offset) if offset else 0
        
    url = await set_url(query)
    myfilter = '--filter illust_ai_type!=2 --range' if '&ai_type=1' in url else '--range'
    
    gallery_dl_result = await gallery_dl(url, pid, filter=myfilter)
    lists = await set_info_dict(gallery_dl_result)
    results = []

    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)

    if lists:
        try:
            for my_list in lists:
                if my_list['extension'] in IMG_EXT:
                    result = InlineQueryResultPhoto(
                        photo_url=my_list['sample_img'],
                        thumb_url=my_list['thumbnail'],
                        id=str(uuid.uuid4()) + my_list['id'],
                        caption=(
                            f"**[{my_list['title']}](https://www.pixiv.net/en/artworks/{my_list['id']})**\n"
                            f"Artist : [{my_list['artist']}](https://www.pixiv.net/en/users/{my_list['artist_id']})\n"
                            f"Tags : {my_list['tags']}"
                        ),
                        reply_markup=await image_keyboard(query, my_list),
                    )

                    results.append(result)
    
            await client.answer_inline_query(
                inline_query.id,
                results=results,
                cache_time=60,
                is_gallery=True,
                next_offset=str(pid + OFFSET_PID)
            )
        except Exception as err:
            logging.error(err)
    


async def get_px_file(url):
    return f"https://i.pximg.net/img-original/img/{url}"


# Perlu decorator premium
async def upload_px_batch(app, message):
    query = str(message.text)
    if not query:
        return
    
    pid = 0
    limit = 30
    asfile = False
    img_slice = 10

    input = query.split()
    for i, val in enumerate(input):
        if 'limit:' in val:
            limit = int(val.split("limit:")[-1].strip())
            limit = limit if limit <= 30 else 30
            query = query.replace(val, '')
        if val.isdigit():
            pid = int(val)
            query = query.replace(val, '')
        if 'as_file' in val:
            asfile = True
            query = query.replace(val, '')

    url = await set_url(query)
    gallery_dl_result = await gallery_dl(url, pid)
    lists = await set_info_dict(gallery_dl_result)

    if not lists:
        return
    
    await app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_PHOTO)
    try:
        for i in range(0, len(lists), img_slice):
            media_to_send = []
            for list in lists[i:i + 10]:
                if list['extension'] in IMG_EXT:
                    if asfile:
                        media_to_send.append(InputMediaDocument(media=list['img_url']))
                    else:
                        media_to_send.append(InputMediaPhoto(media=list['img_url']))

            if media_to_send:
                try:
                    await app.send_media_group(message.chat.id, media_to_send, disable_notification=True)
                except:
                    pass

        await app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
    
    except Exception as err:
        logging.error(err, exc_info=True)
