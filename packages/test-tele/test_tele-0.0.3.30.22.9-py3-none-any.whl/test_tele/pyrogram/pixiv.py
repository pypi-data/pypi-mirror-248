import uuid 
import logging
from pixivpy3 import *
import time

from pyrogram import enums
from pyrogram.types import InputMediaPhoto, InputMediaDocument
from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)

from .utils import IMG_EXT, not_found_msg


async def image_keyboard(query: str, lists: list[str]) -> InlineKeyboardMarkup:
    url = lists['img_urls']['img_original'].split("/img/")[-1]
    buttons = [[
                InlineKeyboardButton("👤🔄",
                                     switch_inline_query_current_chat=f".px id:{lists['user_id']}"),
                InlineKeyboardButton("🔗🔄",
                                     switch_inline_query_current_chat=f".px {lists['id']}")
            ],[
                InlineKeyboardButton("💾" ,
                                     callback_data=f"px {url}"),
                InlineKeyboardButton("🔄",
                                     switch_inline_query_current_chat=query),
            ]]
    return InlineKeyboardMarkup(buttons)


api = AppPixivAPI()
api.auth(refresh_token='FY0E1IOR9NN-ls0O75IXs62QeZvv-CdxLJC6pAZDmfE')


async def get_pixiv_json(query: str, offset: int):
    modes = {
        "-exact": "exact_match_for_tags",
        "-title": "title_and_caption"
    }

    if query != '':
        input = query.split()
        for val in input:
            if val.isdigit() and len(val):
                return 1, api.illust_detail(int(val))
            if 'id:' in val:
                user_id = val.split("id:")[-1]
                return 2, api.user_illusts(int(user_id), offset=offset)
    else:
        # Default = sangonomiya kokomi R18 
        query = '珊瑚宮心海'

    return 0, api.search_illust(query, offset=offset)


async def set_info_dict(cat_json, pixiv_json):
    if cat_json in (0, 2): # search_illust, user_illusts
        illust = pixiv_json.illusts
    elif cat_json == 1:
        illust = pixiv_json.illust
    
    img_urls = []
    if illust.meta_single_page:
        images = {
            "img_thumb": illust.image_urls.square_medium,
            "img_sample": illust.image_urls.medium,
            "img_original": illust.meta_single_page.original_image_url
        }
        img_urls.append(images)
    else:
        for image in illust.meta_pages:
            images = {
                "img_thumb": image.square_medium,
                "img_sample": image.medium,
                "img_original": image.original
            }
            img_urls.append(images)

    media_post = {
        'id': str(illust.id),
        'title': illust.title,
        'user_id': str(illust.user.id),
        'user_name': illust.user.name,
        'tags': await get_pixiv_tags(illust.tags),
        'img_urls': img_urls
    }

    return media_post


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


async def inline_pixiv(client, inline_query):
    """Show Pixiv artworks"""
    query = inline_query.query

    if not query:
        return

    limit = 30
    offset = inline_query.offset
    pid = int(offset) if offset else 0
    query = str(query).strip().lower().replace(".px", "").lstrip()

    cat_json, px_json = await get_pixiv_json(query, pid)
    lists = await set_info_dict(cat_json, px_json)

    results = []

    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)

    if lists:
        try:
            for my_list in lists['img_urls']:
                if str(my_list['img_sample']).endswith(tuple(IMG_EXT)):
                    result = InlineQueryResultPhoto(
                        photo_url=my_list['img_sample'],
                        thumb_url=my_list['img_thumb'],
                        id=str(uuid.uuid4()) + lists['id'],
                        caption=(
                            f"**[{lists['title']}](https://www.pixiv.net/en/artworks/{lists['id']})**\n"
                            f"Artist : [{lists['user_name']}](https://www.pixiv.net/en/users/{lists['user_id']})\n"
                            f"Tags : {lists['tags']}"
                        ),
                        reply_markup=await image_keyboard(query, my_list),
                    )

                    results.append(result)
    
            await client.answer_inline_query(
                inline_query.id,
                results=results,
                cache_time=60,
                is_gallery=True,
                next_offset=str(pid + limit)
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
    
    cat_json, px_json = await get_pixiv_json(query, pid)
    lists = await set_info_dict(cat_json, px_json)

    if not lists:
        return
    
    await app.send_chat_action(chat_id, enums.ChatAction.UPLOAD_PHOTO)
    logging.warning(f"selesai ambil data: {round(time.time() - start, 2)}")
    try:
        for i in range(0, len(lists['img_urls']), img_slice):
            media_to_send = []
            if i + 10 > limit:
                break

            for list in lists['img_urls'][i:i + 10]:
                if str(list['img_sample']).endswith(tuple(IMG_EXT)):
                    if asfile:
                        media_to_send.append(InputMediaDocument(media=list['img_original']))
                    else:
                        media_to_send.append(InputMediaPhoto(media=list['img_sample']))

            if media_to_send:
                try:
                    await app.send_media_group(chat_id, media_to_send, disable_notification=True)
                except:
                    pass
        
        await app.send_chat_action(chat_id, enums.ChatAction.CANCEL)
        logging.warning(f"akhir : {round(time.time() - start, 2)}")
    except Exception as err:
        logging.error(err, exc_info=True)
