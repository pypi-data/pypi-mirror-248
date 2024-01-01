import uuid 
import logging
from pixivpy3 import *
import time

from pyrogram import enums
from pyrogram.types import InputMediaPhoto, InputMediaDocument
from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)

from .utils import IMG_EXT, BOT_CONFIG, not_found_msg


async def image_keyboard(query: str, my_list: list[str]) -> InlineKeyboardMarkup:
    url = my_list['img_urls']['img_original'].split("/img/")[-1]
    buttons = [[
                InlineKeyboardButton("👤🔄",
                                     switch_inline_query_current_chat=f".px id:{my_list['user_id']}"),
                InlineKeyboardButton("🔗🔄",
                                     switch_inline_query_current_chat=f".px {my_list['id']}")
            ],[
                InlineKeyboardButton("💾" ,
                                     callback_data=f"px {url}"),
                InlineKeyboardButton("🔄",
                                     switch_inline_query_current_chat=query),
            ]]
    return InlineKeyboardMarkup(buttons)


api = AppPixivAPI()
api.auth(refresh_token=BOT_CONFIG.apis.pixiv_refresh_token)


async def get_pixiv_list(query: str, offset: int):
    modes = {
        "-exact": "exact_match_for_tags",
        "-title": "title_and_caption"
    }

    if query != '':
        input = query.split()
        for val in input:
            if val.isdigit() and len(val):
                return await set_dict_detail(api.illust_detail(int(val)))
            if 'id:' in val:
                user_id = val.split("id:")[-1]
                return await set_dict_search(api.user_illusts(int(user_id), offset=offset))
    else:
        # Default = sangonomiya kokomi R18 
        query = '珊瑚宮心海'

    return await set_dict_search(api.search_illust(query, offset=offset))


async def set_dict_search(pixiv_json):
    illusts = pixiv_json["illusts"]
    media_posts = []

    for illust in illusts:
        if illust["meta_pages"]:
            img_ori = illust["meta_pages"][0]["image_urls"]["original"]
        else:
            img_ori = illust['meta_single_page']['original_image_url']
            
        images = {
            "img_thumb": illust["image_urls"]["square_medium"],
            "img_sample": illust["image_urls"]["medium"],
            "img_original": img_ori
        }

        media_post = {
            'id': str(illust["id"]),
            'title': illust["title"],
            'user_id': str(illust["user"]["id"]),
            'user_name': illust["user"]["name"],
            'tags': await get_pixiv_tags(illust["tags"]),
            'img_urls': images
        }
        media_posts.append(media_post)

    return media_posts


async def set_dict_detail(pixiv_json):
    illusts = pixiv_json["illust"]
    media_posts = []

    if 'meta_pages' in illusts and illusts['meta_pages']:
        for illust in illusts['meta_pages']:
            images = {
                "img_thumb": illust["image_urls"]["square_medium"],
                "img_sample": illust["image_urls"]["medium"],
                "img_original": illust["image_urls"]["original"]
            }

            media_post = {
                'id': str(illusts["id"]),
                'title': illusts["title"],
                'user_id': str(illusts["user"]["id"]),
                'user_name': illusts["user"]["name"],
                'tags': await get_pixiv_tags(illusts["tags"]),
                'img_urls': images
            }
            media_posts.append(media_post)
    else:
        images['img_original'] = illusts["meta_single_page"]["original_image_url"]
        media_post = {
            'id': str(illusts["id"]),
            'title': illusts["title"],
            'user_id': str(illusts["user"]["id"]),
            'user_name': illusts["user"]["name"],
            'tags': await get_pixiv_tags(illusts["tags"]),
            'img_urls': images
        }
        media_posts.append(media_post)
    return media_posts


async def get_pixiv_tags(tags):
    all_tags = []
    for tag in tags:
        if not tag.translated_name:
            re_tag = f"`{tag.name}`"
        else:
            re_tag = f"`{tag.name}`(`{tag.translated_name}`)"
        all_tags.append(re_tag)
    final_tag = (", ").join(all_tags)
    return final_tag


async def set_caption(my_list, no_tag=False):
    if no_tag:
        caption = ''
    else:
        caption = (
            f"**[{my_list['title']}](https://www.pixiv.net/en/artworks/{my_list['id']})**\n"
            f"Artist : [{my_list['user_name']}](https://www.pixiv.net/en/users/{my_list['user_id']})\n"
            f"Tags : {my_list['tags']}"
        )
    return caption


async def inline_pixiv(client, inline_query):
    """Show Pixiv artworks"""
    query = inline_query.query

    if not query:
        return

    limit = 30
    no_tag = False
    offset = inline_query.offset
    pid = int(offset) if offset else 0
    keyword = str(query).strip().lower().replace(".px", "").lstrip()

    if 'no_tag' in query:
        no_tag = True
        keyword = keyword.replace('no_tag', '')

    lists = await get_pixiv_list(query, pid)

    results = []

    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)

    if lists:
        try:
            for my_list in lists:
                if str(my_list['img_urls']['img_sample']).endswith(tuple(IMG_EXT)):
                    result = InlineQueryResultPhoto(
                        photo_url=my_list['img_urls']['img_sample'],
                        thumb_url=my_list['img_urls']['img_thumb'],
                        id=str(uuid.uuid4()) + my_list['id'],
                        caption=await set_caption(my_list, no_tag),
                        reply_markup=await image_keyboard(query, my_list),
                    )

                    results.append(result)

            await client.answer_inline_query(
                inline_query.id,
                results=results,
                cache_time=60,
                is_gallery=True,
                next_offset=str(pid + limit) if len(lists) > 30 else None
            )
        except Exception as err:
            logging.error(err, exc_info=True)
    

async def get_px_file(url):
    return f"https://i.pximg.net/img-original/img/{url}"


# Perlu decorator premium
async def upload_px_batch(app, message):
    query = str(message.text)
    if not query:
        return
    start = time.time()
    pid = 0
    limit = 30
    chat_id = message.chat.id
    asfile = False
    img_slice = 10
    query = str(query).strip().lower().replace(".px", "").lstrip()

    if query != '':
        input = query.split()
        for i, val in enumerate(input):
            if 'limit:' in val:
                limit = int(val.split("limit:")[-1].strip())
                limit = limit if limit <= 30 else 30
                query = query.replace(val, '')
            if 'offset:' in val:
                pid = int(val.split("offset:")[-1].strip())
                query = query.replace(val, '')
            if 'as_file' in val:
                asfile = True
                query = query.replace(val, '')
    
    lists = await get_pixiv_list(query, pid)

    if not lists:
        return
    
    await app.send_chat_action(chat_id, enums.ChatAction.UPLOAD_PHOTO)
    logging.warning(f"selesai ambil data: {round(time.time() - start, 2)}")
    try:
        for i in range(0, len(lists), img_slice):
            media_to_send = []
            if i + 10 > limit:
                break

            for list in lists[i:i + 10]:
                if str(list['img_urls']['img_sample']).endswith(tuple(IMG_EXT)):
                    if asfile:
                        media_to_send.append(InputMediaDocument(media=list['img_urls']['img_original']))
                    else:
                        media_to_send.append(InputMediaPhoto(media=list['img_urls']['img_sample']))

            if media_to_send:
                try:
                    await app.send_media_group(chat_id, media_to_send, disable_notification=True)
                except:
                    pass
        
        await app.send_chat_action(chat_id, enums.ChatAction.CANCEL)
        logging.warning(f"akhir : {round(time.time() - start, 2)}")
    except Exception as err:
        logging.error(err, exc_info=True)
