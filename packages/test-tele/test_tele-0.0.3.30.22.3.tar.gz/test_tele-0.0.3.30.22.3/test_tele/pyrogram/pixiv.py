import uuid 
import logging
from pixivpy3 import *

from pyrogram import enums
from pyrogram.types import InputMediaPhoto, InputMediaDocument
from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)

from .utils import OFFSET_PID, IMG_EXT, not_found_msg


async def image_keyboard(query: str, my_list: list[str]) -> InlineKeyboardMarkup:
    url = my_list['file'].split("/img/")[-1]
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
api.auth(refresh_token='FY0E1IOR9NN-ls0O75IXs62QeZvv-CdxLJC6pAZDmfE')


async def get_pixiv_json(query: str, offset: int):
    modes = {
        "-exact": "exact_match_for_tags",
        "-title": "title_and_caption"
    }

    input = query.split()
    for val in input:
        if val.isdigit() and len(val):
            return api.illust_detail(int(val))
        if 'id:' in val:
            user_id = val.split("id:")[-1]
            return api.user_illusts(int(user_id))
    
    # Default = sangonomiya kokomi R18 
    if query == "":
        query = '珊瑚宮心海'

    return api.search_illust(query, offset=offset)


async def set_info_dict(pixiv_json):
    posts = []
    for illust in pixiv_json.illusts:
        media_post = {}
        media_post['id'] = illust.id
        media_post['title'] = illust.title
        media_post['thumbnail'] = illust.image_urls.square_medium
        media_post['sample'] = illust.image_urls.medium
        media_post['file'] = illust.meta_single_page.original_image_url
        media_post['user_id'] = illust.user.id
        media_post['user_name'] = illust.user.name
        media_post['tags'] = await get_pixiv_tags(illust.tags)
        posts.append(media_post)


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
        
    px_json = await get_pixiv_json(query, pid)
    lists = await set_info_dict(px_json)
    results = []

    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)

    if lists:
        try:
            for my_list in lists:
                if str(my_list['sample']).endswith(tuple(IMG_EXT)):
                    result = InlineQueryResultPhoto(
                        photo_url=my_list['sample'],
                        thumb_url=my_list['thumbnail'],
                        id=str(uuid.uuid4()) + my_list['id'],
                        caption=(
                            f"**[{my_list['title']}](https://www.pixiv.net/en/artworks/{my_list['id']})**\n"
                            f"Artist : [{my_list['user_name']}](https://www.pixiv.net/en/users/{my_list['user_id']})\n"
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
                next_offset=str(pid + limit)
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
    chat_id = message.chat.id
    asfile = False
    img_slice = 10
    query = str(query).strip().lower().replace(".px", "").lstrip()

    input = query.split()
    for i, val in enumerate(input):
        if 'limit:' in val:
            limit = int(val.split("limit:")[-1].strip())
            limit = limit if limit <= 30 else 30
            query = query.replace(val, '')
        if 'offset:':
            pid = int(val.split("offset:")[-1].strip())
            query = query.replace(val, '')
        if 'as_file' in val:
            asfile = True
            query = query.replace(val, '')

    px_json = await get_pixiv_json(query, pid)
    lists = await set_info_dict(px_json)

    if not lists:
        return
    
    await app.send_chat_action(chat_id, enums.ChatAction.UPLOAD_PHOTO)
    try:
        for i in range(0, len(lists), img_slice):
            media_to_send = []
            if i + 10 >= limit:
                break
            
            for list in lists[i:i + 10]:
                if str(list['sample']).endswith(tuple(IMG_EXT)):
                    if asfile:
                        media_to_send.append(InputMediaDocument(media=list['file']))
                    else:
                        media_to_send.append(InputMediaPhoto(media=list['sample']))

            if media_to_send:
                try:
                    await app.send_media_group(chat_id, media_to_send, disable_notification=True)
                except:
                    pass

        await app.send_chat_action(chat_id, enums.ChatAction.CANCEL)
    
    except Exception as err:
        logging.error(err, exc_info=True)
