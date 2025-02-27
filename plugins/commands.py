import os
import logging
import random
import asyncio
import pytz
from Script import script
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import *
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db
from info import CHANNELS, ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT_ID, SUPPORT_CHAT, MAX_B_TN, VERIFY, HOWTOVERIFY, SHORTLINK_API, SHORTLINK_URL, TUTORIAL, IS_TUTORIAL, PREMIUM_USER, PICS, SUBSCRIPTION
from utils import get_settings, get_size, is_req_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token, get_shortlink, get_tutorial
from database.connections_mdb import active_connection
# from plugins.pm_filter import ENABLE_SHORTLINK
import re, asyncio, os, sys
import json
import base64
logger = logging.getLogger(__name__)

TIMEZONE = "Asia/Kolkata"
BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
                    InlineKeyboardButton('☆ 𝗔𝗱𝗱 𝗠𝗲 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽 ☆', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('🍁 𝗛𝗼𝘄 𝗧𝗼 𝗨𝘀𝗲 𝗠𝗲 🍁', url="https://t.me/{temp.U_NAME}?start=help")
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.GSTART_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup, disable_web_page_preview=True)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
                    InlineKeyboardButton('🎥 𝗠𝗼𝘃𝗶𝗲 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗚𝗿𝗼𝘂𝗽 📽', url=f'https://t.me/+ZUyhAwBNBsU0YjA9')
                ],[
                    InlineKeyboardButton('☆ 𝗔𝗱𝗱 𝗠𝗲 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽 ☆', url=f'http://telegram.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('💸 𝗘𝗮𝗿𝗻 𝗠𝗼𝗻𝗲𝘆 💸', callback_data="shortlink_info"),
                    InlineKeyboardButton('• 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 •', callback_data='channels')
                ],[
                    InlineKeyboardButton('• 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 •', callback_data='help'),
                    InlineKeyboardButton('• 𝗔𝗯𝗼𝘂𝘁 •', callback_data='about')
                ],[
                    InlineKeyboardButton('✨ 𝗕𝘂𝘆 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 : 𝗥𝗲𝗺𝗼𝘃𝗲 𝗔𝗱𝘀 ✨', callback_data="premium_info")
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "𝖦𝗈𝗈𝖽 𝖬𝗈𝗋𝗇𝗂𝗇𝗀 👋" 
        elif curr_time < 17:
            gtxt = "𝖦𝗈𝗈𝖽 𝖠𝖿𝗍𝖾𝗋𝗇𝗈𝗈𝗇 👋" 
        elif curr_time < 21:
            gtxt = "𝖦𝗈𝗈𝖽 𝖤𝗏𝖾𝗇𝗂𝗇𝗀 👋"
        else:
            gtxt = "𝖦𝗈𝗈𝖽 𝖭𝗂𝗀𝗁𝗍 👋"
        m=await message.reply_text("<i>𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖳𝗈 𝗔𝗹𝗹 𝗠𝗼𝘃𝗶𝗲𝘀 𝗟𝗶𝗻𝗸 𝗕𝗼𝘁.</i>")
        await asyncio.sleep(0.4)
        await m.edit_text("👀")
        await asyncio.sleep(0.5)
        await m.edit_text("⚡")
        await asyncio.sleep(0.5)
        await m.edit_text("<b><i>𝖲𝗍𝖺𝗋𝗍𝗂𝗇𝗀...</i></b>")
        await asyncio.sleep(0.4)
        await m.delete()
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, gtxt, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
        
    if AUTH_CHANNEL and not await is_req_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL), creates_join_request=True)
        except ChatAdminRequired:
            logger.error("Make sure the bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "📌 𝗝𝗼𝗶𝗻 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 📌", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)
                btn.append([InlineKeyboardButton("↻ 𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻", callback_data=f"checksub#{kk}#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton("↻ 𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text="𝖩𝗈𝗂𝗇 𝖮𝗎𝗋 𝖴𝗉𝖽𝖺𝗍𝖾𝗌 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖺𝗇𝖽 𝖳𝗁𝖾𝗇 𝖢𝗅𝗂𝖼𝗄 𝗈𝗇 𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻 𝗍𝗈 𝖦𝖾𝗍 𝖸𝗈𝗎𝗋 𝖱𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖥𝗂𝗅𝖾.",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
            )
        return
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
                    InlineKeyboardButton('🎥 𝗠𝗼𝘃𝗶𝗲 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗚𝗿𝗼𝘂𝗽 📽', url=f'https://t.me/+ZUyhAwBNBsU0YjA9')
                ],[
                    InlineKeyboardButton('☆ 𝗔𝗱𝗱 𝗠𝗲 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽 ☆', url=f'http://telegram.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('💸 𝗘𝗮𝗿𝗻 𝗠𝗼𝗻𝗲𝘆 💸', callback_data="shortlink_info"),
                    InlineKeyboardButton('• 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 •', callback_data='channels')
                ],[
                    InlineKeyboardButton('• 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 •', callback_data='help'),
                    InlineKeyboardButton('• 𝗔𝗯𝗼𝘂𝘁 •', callback_data='about')
                ],[
                    InlineKeyboardButton('✨ 𝗕𝘂𝘆 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 : 𝗥𝗲𝗺𝗼𝘃𝗲 𝗔𝗱𝘀 ✨', callback_data="premium_info")
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "𝖦𝗈𝗈𝖽 𝖬𝗈𝗋𝗇𝗂𝗇𝗀 👋" 
        elif curr_time < 17:
            gtxt = "𝖦𝗈𝗈𝖽 𝖠𝖿𝗍𝖾𝗋𝗇𝗈𝗈𝗇 👋" 
        elif curr_time < 21:
            gtxt = "𝖦𝗈𝗈𝖽 𝖤𝗏𝖾𝗇𝗂𝗇𝗀 👋"
        else:
            gtxt = "𝖦𝗈𝗈𝖽 𝖭𝗂𝗀𝗁𝗍 👋"
        m=await message.reply_text("<i>𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝖳𝗈 𝗔𝗹𝗹 𝗠𝗼𝘃𝗶𝗲𝘀 𝗟𝗶𝗻𝗸 𝗕𝗼𝘁.</i>")
        await asyncio.sleep(0.4)
        await m.edit_text("👀")
        await asyncio.sleep(0.5)
        await m.edit_text("⚡")
        await asyncio.sleep(0.5)
        await m.edit_text("<b><i>𝖲𝗍𝖺𝗋𝗍𝗂𝗇𝗀...</i></b>")
        await asyncio.sleep(0.4)
        await m.delete()
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, gtxt, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
        
        
    if len(message.command) == 2 and message.command[1] in ["premium"]:
        buttons = [[
                    InlineKeyboardButton('📲 𝗦𝗲𝗻𝗱 𝗣𝗮𝘆𝗺𝗲𝗻𝘁 𝗦𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁', user_id=int(1101724431))
                  ],[
                    InlineKeyboardButton('❌ 𝗖𝗹𝗼𝘀𝗲 ❌', callback_data='close_data')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=(SUBSCRIPTION),
            caption=script.PREPLANS_TXT.format(message.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return  
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""
    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply("<b>𝖯𝗅𝖾𝖺𝗌𝖾 𝖶𝖺𝗂𝗍...</b>")
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await client.download_media(file_id)
            try:
                with open(file) as file_data:
                    msgs = json.loads(file_data.read())
            except:
                await sts.edit("FAILED")
                return await client.send_message(LOG_CHANNEL, "UNABLE TO OPEN FILE.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs
        messages_to_delete = []
        for msg in msgs:
            title = msg.get("title")
            size = get_size(int(msg.get("size", 0)))
            f_caption = msg.get("caption", "")
            if BATCH_FILE_CAPTION:
                try:
                    f_caption = BATCH_FILE_CAPTION.format(
                        file_name='' if title is None else title,
                        file_size='' if size is None else size,
                        file_caption='' if f_caption is None else f_caption
                    )
                except Exception as e:
                    logger.exception(e)
                    f_caption = f_caption
            if f_caption is None:
                f_caption = f"{title}"
            try:
                sent_msg = await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    '🎥 𝗝𝗼𝗶𝗻 𝗠𝗼𝘃𝗶𝗲 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗚𝗿𝗼𝘂𝗽 🎥',
                                    url=f'https://t.me/+pp_D21tjCtAzMjc1'
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    '📌 𝗝𝗼𝗶𝗻 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 📌',
                                    url=f'https://t.me/+QgSl55NlTiI0NDhl'
                                )
                            ]
                        ]
                    )
                )
                messages_to_delete.append(sent_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                continue
            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            await asyncio.sleep(1)
        notify_msg = await client.send_message(
            chat_id=message.from_user.id,
            text=(
                "<b>❗️ <u>𝖨𝗆𝗉𝗈𝗋𝗍𝖺𝗇𝗍</u> ❗️</b>\n\n"
                "<b>𝖳𝗁𝖾𝗌𝖾 𝖿𝗂𝗅𝖾𝗌 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗂𝗇</b> "
                "<b><u>10 𝖬𝗂𝗇𝗎𝗍𝖾𝗌</u></b>.\n\n"
                "<b><i>📌 𝖯𝗅𝖾𝖺𝗌𝖾 𝗦𝗮𝘃𝗲 𝖮𝗋 𝖥𝗈𝗋𝗐𝖺𝗋𝖽 𝖳𝗁𝖾𝗌𝖾 𝖥𝗂𝗅𝖾𝗌 𝗍𝗈 𝗦𝗮𝘃𝗲𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝖲𝗈𝗈𝗇.</i></b>"
            )
        )
        await sts.delete()
        await asyncio.sleep(600)
        for sent_msg in messages_to_delete:
            await sent_msg.delete()
        await notify_msg.edit_text(
            "<b>🗑️ 𝖠𝗅𝗅 𝖿𝗂𝗅𝖾𝗌 𝗁𝖺𝗏𝖾 𝖻𝖾𝖾𝗇 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒! 𝖪𝗂𝗇𝖽𝗅𝗒 𝖼𝗅𝗂𝖼𝗄 𝗍𝗁𝖾 𝗅𝗂𝗇𝗄 𝖺𝗀𝖺𝗂𝗇 𝗂𝖿 𝗇𝖾𝖾𝖽𝖾𝖽.</b>"
        )
        return

    
    elif data.split("-", 1)[0] == "DSTORE":
        sts = await message.reply("<b>𝖯𝗅𝖾𝖺𝗌𝖾 𝖶𝖺𝗂𝗍...</b>")
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        try:
            f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
        except:
            f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
            protect = "/pbatch" if PROTECT_CONTENT else "batch"
        diff = int(l_msg_id) - int(f_msg_id)
        async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
            if msg.media:
                media = getattr(msg, msg.media.value)
                if BATCH_FILE_CAPTION:
                    try:
                        f_caption=BATCH_FILE_CAPTION.format(file_name=getattr(media, 'file_name', ''), file_size=getattr(media, 'file_size', ''), file_caption=getattr(msg, 'caption', ''))
                    except Exception as e:
                        logger.exception(e)
                        f_caption = getattr(msg, 'caption', '')
                else:
                    media = getattr(msg, msg.media.value)
                    file_name = getattr(media, 'file_name', '')
                    f_caption = getattr(msg, 'caption', file_name)
                try:
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            elif msg.empty:
                continue
            else:
                try:
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            await asyncio.sleep(1) 
        return await sts.delete()

    elif data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗅𝗂𝗇𝗄 𝗈𝗋 𝖤𝗑𝗉𝗂𝗋𝖾𝖽 𝗅𝗂𝗇𝗄!</b>",
                protect_content=True
            )
        is_valid = await check_token(client, userid, token)
        if is_valid == True:
            await message.reply_text(
                text=f"<b>𝖧𝖾𝗒 {message.from_user.mention}, 𝖸𝗈𝗎 𝖺𝗋𝖾 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗏𝖾𝗋𝗂𝖿𝗂𝖾𝖽!\n𝖭𝗈𝗐 𝗒𝗈𝗎 𝗁𝖺𝗏𝖾 𝗎𝗇𝗅𝗂𝗆𝗂𝗍𝖾𝖽 𝖺𝖼𝖼𝖾𝗌𝗌 𝖿𝗈𝗋 𝖺𝗅𝗅 𝖿𝗂𝗅𝖾𝗌 𝗍𝗂𝗅𝗅 𝗍𝗈𝖽𝖺𝗒 𝗆𝗂𝖽𝗇𝗂𝗀𝗁𝗍.</b>",
                protect_content=True
            )
            await verify_user(client, userid, token)
        else:
            return await message.reply_text(
                text="<b>𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗅𝗂𝗇𝗄 𝗈𝗋 𝖤𝗑𝗉𝗂𝗋𝖾𝖽 𝗅𝗂𝗇𝗄!</b>",
                protect_content=True
            )
    if data.startswith("sendfiles"):
        protect_content=True
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "𝖦𝗈𝗈𝖽 𝖬𝗈𝗋𝗇𝗂𝗇𝗀 👋" 
        elif curr_time < 17:
            gtxt = "𝖦𝗈𝗈𝖽 𝖠𝖿𝗍𝖾𝗋𝗇𝗈𝗈𝗇 👋" 
        elif curr_time < 21:
            gtxt = "𝖦𝗈𝗈𝖽 𝖤𝗏𝖾𝗇𝗂𝗇𝗀 👋"
        else:
            gtxt = "𝖦𝗈𝗈𝖽 𝖭𝗂𝗀𝗁𝗍 👋"
        chat_id = int("-" + file_id.split("-")[1])
        userid = message.from_user.id if message.from_user else None
        g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=allfiles_{file_id}")
        k = await client.send_message(chat_id=message.from_user.id,text=f"🫂 𝖧𝖾𝗒 {message.from_user.mention}, {gtxt}\n\n‼️ 𝖦𝖾𝗍 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 𝗂𝗇 𝖺 𝖲𝗂𝗇𝗀𝗅𝖾 𝖫𝗂𝗇𝗄 ‼️\n\n✅ 𝖸𝗈𝗎𝗋 𝖫𝗂𝗇𝗄 𝗂𝗌 𝖱𝖾𝖺𝖽𝗒, 𝖪𝗂𝗇𝖽𝗅𝗒 𝖢𝗅𝗂𝖼𝗄 𝗈𝗇 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝖡𝗎𝗍𝗍𝗈𝗇.\n\n", reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('📁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 📁', url=g)
                    ], [
                        InlineKeyboardButton('⚡ 𝗛𝗼𝘄 𝘁𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 ⚡', url=await get_tutorial(chat_id))
                    ], [
                        InlineKeyboardButton('✨ 𝗕𝘂𝘆 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 : 𝗥𝗲𝗺𝗼𝘃𝗲 𝗔𝗱𝘀 ✨', callback_data="seeplans")                        
                    ]
                ]
            )
        )
        await asyncio.sleep(300)
        await k.edit("<b>🗑️ 𝖠𝗅𝗅 𝖿𝗂𝗅𝖾𝗌 𝗁𝖺𝗏𝖾 𝖻𝖾𝖾𝗇 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒! 𝖪𝗂𝗇𝖽𝗅𝗒 𝗌𝖾𝖺𝗋𝖼𝗁 𝖺𝗀𝖺𝗂𝗇 𝗂𝖿 𝗇𝖾𝖾𝖽𝖾𝖽.</b>")
        return
        
    
    elif data.startswith("short"):
        protect_content=True
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "𝖦𝗈𝗈𝖽 𝖬𝗈𝗋𝗇𝗂𝗇𝗀 👋" 
        elif curr_time < 17:
            gtxt = "𝖦𝗈𝗈𝖽 𝖠𝖿𝗍𝖾𝗋𝗇𝗈𝗈𝗇 👋" 
        elif curr_time < 21:
            gtxt = "𝖦𝗈𝗈𝖽 𝖤𝗏𝖾𝗇𝗂𝗇𝗀 👋"
        else:
            gtxt = "𝖦𝗈𝗈𝖽 𝖭𝗂𝗀𝗁𝗍 👋"        
        user_id = message.from_user.id
        chat_id = temp.SHORT.get(user_id)
        files_ = await get_file_details(file_id)
        files = files_[0]
        g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
        k = await client.send_message(
            chat_id=user_id,
            text=f"🫂 𝖧𝖾𝗒 {message.from_user.mention}, {gtxt}\n\n✅ 𝖸𝗈𝗎𝗋 𝖫𝗂𝗇𝗄 𝗂𝗌 𝖱𝖾𝖺𝖽𝗒, 𝖪𝗂𝗇𝖽𝗅𝗒 𝖢𝗅𝗂𝖼𝗄 𝗈𝗇 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝖡𝗎𝗍𝗍𝗈𝗇.\n\n⚠️ 𝖥𝗂𝗅𝖾 𝖭𝖺𝗆𝖾 : <code>{files.file_name}</code> \n\n📥 𝖥𝗂𝗅𝖾 𝖲𝗂𝗓𝖾 : <code>{get_size(files.file_size)}</code>\n\n",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('📁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 📁', url=g)
                ], [
                    InlineKeyboardButton('⚡ 𝗛𝗼𝘄 𝘁𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 ⚡', url=await get_tutorial(chat_id))
                ], [
                    InlineKeyboardButton('✨ 𝗕𝘂𝘆 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 : 𝗥𝗲𝗺𝗼𝘃𝗲 𝗔𝗱𝘀 ✨', callback_data="seeplans")
                ]]
            )
        )
        await asyncio.sleep(600)
        await k.edit("<b>𝖸𝗈𝗎𝗋 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝗂𝗌 𝖣𝖾𝗅𝖾𝗍𝖾𝖽!\n𝖪𝗂𝗇𝖽𝗅𝗒 𝖲𝖾𝖺𝗋𝖼𝗁 𝖠𝗀𝖺𝗂𝗇.</b>")
        return
        
    elif data.startswith("all"):
        protect_content=True
        user_id = message.from_user.id
        files = temp.GETALL.get(file_id)
        if not files:
            return await message.reply('<b><i>𝖭𝗈 𝖲𝗎𝖼𝗁 𝖥𝗂𝗅𝖾 𝖤𝗑𝗂𝗌𝗍𝗌!</b></i>')
        filesarr = []
        for file in files:
            file_id = file.file_id
            files_ = await get_file_details(file_id)
            files1 = files_[0]
            title = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1.file_name.split()))
            size=get_size(files1.file_size)
            f_caption=files1.caption
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=f_caption
            if f_caption is None:
                f_caption = f"{' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1.file_name.split()))}"

            if not await check_verification(client, message.from_user.id) and VERIFY == True:
                btn = [[
                    InlineKeyboardButton("♻️ 𝗖𝗹𝗶𝗰𝗸 𝗵𝗲𝗿𝗲 𝘁𝗼 𝘃𝗲𝗿𝗶𝗳𝘆 ♻️", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start="))
                ],[
                    InlineKeyboardButton("⁉️ 𝗛𝗼𝘄 𝘁𝗼 𝘃𝗲𝗿𝗶𝗳𝘆 ⁉️", url=HOWTOVERIFY)
                ]]
                await message.reply_text(
                    text="<b>👋 𝖧𝖾𝗒 {message.from_user.mention}, 𝖸𝗈𝗎 𝖺𝗋𝖾 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗏𝖾𝗋𝗂𝖿𝗂𝖾𝖽 ✅\n\n𝖭𝗈𝗐 𝗒𝗈𝗎'𝗏𝖾 𝗎𝗇𝗅𝗂𝗆𝗂𝗍𝖾𝖽 𝖺𝖼𝖼𝖾𝗌𝗌 𝗍𝗂𝗅𝗅 𝗇𝖾𝗑𝗍 𝗏𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 🎉</b>",
                    protect_content=True,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                caption=f_caption,
                protect_content=True if pre == 'filep' else False,
                reply_markup=InlineKeyboardMarkup(
            [
             [
              InlineKeyboardButton('🚀 𝗙𝗮𝘀𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 / 𝗪𝗮𝘁𝗰𝗵 𝗢𝗻𝗹𝗶𝗻𝗲 🧿', callback_data=f'generate_stream_link:{file_id}'),
             ],
             [
              InlineKeyboardButton('📌 𝗝𝗼𝗶𝗻 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 📌', url=f'https://t.me/+QgSl55NlTiI0NDhl') #Don't change anything without contacting me @LazyDeveloperr
             ]
            ]
        )
    )
            filesarr.append(msg)
        k = await client.send_message(chat_id = message.from_user.id, text=f"<b>❗️ <u>𝖨𝗆𝗉𝗈𝗋𝗍𝖺𝗇𝗍</u> ❗️</b>\n\n<b>𝖳𝗁𝖾𝗌𝖾 𝖵𝗂𝖽𝖾𝗈𝗌 / 𝖥𝗂𝗅𝖾𝗌 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗂𝗇</b> <b><u>10 𝖬𝗂𝗇𝗎𝗍𝖾𝗌</u> </b><b>(𝖣𝗎𝖾 𝗍𝗈 𝖢𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝖨𝗌𝗌𝗎𝖾𝗌).</b>\n\n<b><i>📌 Please Forward these Videos / Files to 𝗦𝗮𝘃𝗲𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀 and start downloading there.</i></b>")
        await asyncio.sleep(600)
        for x in filesarr:
            await x.delete()
        await k.edit_text("<b>🗑️ 𝖠𝗅𝗅 𝖿𝗂𝗅𝖾𝗌 𝗁𝖺𝗏𝖾 𝖻𝖾𝖾𝗇 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒! 𝖪𝗂𝗇𝖽𝗅𝗒 𝗌𝖾𝖺𝗋𝖼𝗁 𝖺𝗀𝖺𝗂𝗇 𝗂𝖿 𝗇𝖾𝖾𝖽𝖾𝖽.</b>")
        return
        
    elif data.startswith("files"):
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "𝖦𝗈𝗈𝖽 𝖬𝗈𝗋𝗇𝗂𝗇𝗀 👋" 
        elif curr_time < 17:
            gtxt = "𝖦𝗈𝗈𝖽 𝖠𝖿𝗍𝖾𝗋𝗇𝗈𝗈𝗇 👋" 
        elif curr_time < 21:
            gtxt = "𝖦𝗈𝗈𝖽 𝖤𝗏𝖾𝗇𝗂𝗇𝗀 👋"
        else:
            gtxt = "𝖦𝗈𝗈𝖽 𝖭𝗂𝗀𝗁𝗍 👋"        
        user_id = message.from_user.id
        if temp.SHORT.get(user_id)==None:
            return await message.reply_text(text="<b>𝖯𝗅𝖾𝖺𝗌𝖾 𝖲𝖾𝖺𝗋𝖼𝗁 𝖠𝗀𝖺𝗂𝗇 𝗂𝗇 𝖦𝗋𝗈𝗎𝗉</b>")
        else:
            chat_id = temp.SHORT.get(user_id)
        settings = await get_settings(chat_id)
        if not await db.has_premium_access(user_id) and settings['is_shortlink']: #Don't change anything without my permission @CoderluffyTG
            files_ = await get_file_details(file_id)
            files = files_[0]
            g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
            k = await client.send_message(chat_id=message.from_user.id,text=f"🫂 𝖧𝖾𝗒 {message.from_user.mention}, {gtxt}\n\n✅ 𝖸𝗈𝗎𝗋 𝖫𝗂𝗇𝗄 𝗂𝗌 𝖱𝖾𝖺𝖽𝗒, 𝖪𝗂𝗇𝖽𝗅𝗒 𝖢𝗅𝗂𝖼𝗄 𝗈𝗇 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝖡𝗎𝗍𝗍𝗈𝗇.\n\n⚠️ 𝖥𝗂𝗅𝖾 𝖭𝖺𝗆𝖾 : <code>{files.file_name}</code> \n\n📥 𝖥𝗂𝗅𝖾 𝖲𝗂𝗓𝖾 : <code>{get_size(files.file_size)}</code>\n\n", reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('📁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 📁', url=g)
                        ], [
                            InlineKeyboardButton('⚡ 𝗛𝗼𝘄 𝘁𝗼 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 ⚡', url=await get_tutorial(chat_id))
                        ], [
                            InlineKeyboardButton('✨ 𝗕𝘂𝘆 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 : 𝗥𝗲𝗺𝗼𝘃𝗲 𝗔𝗱𝘀 ✨', callback_data="seeplans")                            
                        ]
                    ]
                )
            )
            await asyncio.sleep(600)
            await k.edit("<b>𝖸𝗈𝗎𝗋 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝗂𝗌 𝖣𝖾𝗅𝖾𝗍𝖾𝖽!\n𝖪𝗂𝗇𝖽𝗅𝗒 𝖲𝖾𝖺𝗋𝖼𝗁 𝖠𝗀𝖺𝗂𝗇.</b>")
            return
    user = message.from_user.id
    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            if not await check_verification(client, message.from_user.id) and VERIFY == True:
                btn = [[
                    InlineKeyboardButton("♻️ 𝗖𝗹𝗶𝗰𝗸 𝗵𝗲𝗿𝗲 𝘁𝗼 𝘃𝗲𝗿𝗶𝗳𝘆 ♻️", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start="))
                ],[
                    InlineKeyboardButton("⁉️ 𝗛𝗼𝘄 𝘁𝗼 𝘃𝗲𝗿𝗶𝗳𝘆 ⁉️", url=HOWTOVERIFY)
                ]]
                await message.reply_text(
                    text="<b>👋 𝖧𝖾𝗒 𝗍𝗁𝖾𝗋𝖾,\n\n📌 <u>𝖸𝗈𝗎'𝗋𝖾 𝗇𝗈𝗍 𝗏𝖾𝗋𝗂𝖿𝗂𝖾𝖽 𝗍𝗈𝖽𝖺𝗒, 𝗉𝗅𝖾𝖺𝗌𝖾 𝗏𝖾𝗋𝗂𝖿𝗒 𝖺𝗇𝖽 𝗀𝖾𝗍 𝗎𝗇𝗅𝗂𝗆𝗂𝗍𝖾𝖽 𝖺𝖼𝖼𝖾𝗌𝗌 𝗍𝗂𝗅𝗅 𝗇𝖾𝗑𝗍 𝗏𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇.</u></b>",
                    protect_content=True,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                reply_markup=InlineKeyboardMarkup(
            [
             [
              InlineKeyboardButton('🚀 𝗙𝗮𝘀𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 / 𝗪𝗮𝘁𝗰𝗵 𝗢𝗻𝗹𝗶𝗻𝗲 🧿', callback_data=f'generate_stream_link:{file_id}'),
             ],
             [
              InlineKeyboardButton('📌 𝗝𝗼𝗶𝗻 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 📌', url=f'https://t.me/+QgSl55NlTiI0NDhl') #Don't change anything without contacting me @LazyDeveloperr
             ]
            ]
        )
    )
            filetype = msg.media
            file = getattr(msg, filetype.value)
            title = '' + ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), file.file_name.split()))
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(caption=f_caption,
                                   reply_markup=InlineKeyboardMarkup(
            [
             [
              InlineKeyboardButton('🚀 𝗙𝗮𝘀𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 / 𝗪𝗮𝘁𝗰𝗵 𝗢𝗻𝗹𝗶𝗻𝗲 🧿', callback_data=f'generate_stream_link:{file_id}'),
             ],
             [
              InlineKeyboardButton('📌 𝗝𝗼𝗶𝗻 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 📌', url=f'https://t.me/+QgSl55NlTiI0NDhl') #Don't change anything without contacting me @LazyDeveloperr
             ]
            ]
                                                                     )
            )
            btn = [[
                InlineKeyboardButton("❗ 𝗚𝗲𝘁 𝗙𝗶𝗹𝗲 𝗔𝗴𝗮𝗶𝗻 ❗", callback_data=f'delfile#{file_id}')
            ]]
            k = await client.send_message(chat_id = message.from_user.id, text=f"<b>❗️ <u>𝖨𝗆𝗉𝗈𝗋𝗍𝖺𝗇𝗍</u> ❗️</b>\n\n<b>𝖳𝗁𝗂𝗌 𝖵𝗂𝖽𝖾𝗈 / 𝖥𝗂𝗅𝖾 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗂𝗇</b> <b><u>10 𝖬𝗂𝗇𝗎𝗍𝖾𝗌</u> </b><b>(𝖣𝗎𝖾 𝗍𝗈 𝖢𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝖨𝗌𝗌𝗎𝖾𝗌).</b>\n\n<b><i>📌 𝖯𝗅𝖾𝖺𝗌𝖾 𝖥𝗈𝗋𝗐𝖺𝗋𝖽 𝗍𝗁𝗂𝗌 𝖵𝗂𝖽𝖾𝗈 / 𝖥𝗂𝗅𝖾 𝗍𝗈 𝗦𝗮𝘃𝗲𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝖺𝗇𝖽 𝖲𝗍𝖺𝗋𝗍 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝗍𝗁𝖾𝗋𝖾.</i></b>")
            await asyncio.sleep(600)
            await msg.delete()
            await k.edit_text("<b>𝖸𝗈𝗎𝗋 𝖵𝗂𝖽𝖾𝗈 / 𝖥𝗂𝗅𝖾 𝗂𝗌 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽!!\n\n𝖢𝗅𝗂𝖼𝗄 𝖻𝖾𝗅𝗈𝗐 𝖻𝗎𝗍𝗍𝗈𝗇 𝗍𝗈 𝗀𝖾𝗍 𝗒𝗈𝗎𝗋 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖵𝗂𝖽𝖾𝗈 / 𝖥𝗂𝗅𝖾 𝖠𝗀𝖺𝗂𝗇 👇</b>",reply_markup=InlineKeyboardMarkup(btn))
            return
        except:
            pass
        return await message.reply('𝖭𝗈 𝖲𝗎𝖼𝗁 𝖥𝗂𝗅𝖾 𝖤𝗑𝗂𝗌𝗍𝗌!')
    files = files_[0]
    title = '' + ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files.file_name.split()))
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f" {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files.file_name.split()))}"

    if not await check_verification(client, message.from_user.id) and VERIFY == True:
        btn = [[
            InlineKeyboardButton("♻️ 𝗖𝗹𝗶𝗰𝗸 𝗵𝗲𝗿𝗲 𝘁𝗼 𝘃𝗲𝗿𝗶𝗳𝘆 ♻️", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start="))
        ],[
            InlineKeyboardButton("⁉️ 𝗛𝗼𝘄 𝘁𝗼 𝘃𝗲𝗿𝗶𝗳𝘆 ⁉️", url=HOWTOVERIFY)
        ]]
        await message.reply_text(
            text="<b>👋 𝖧𝖾𝗒 𝗍𝗁𝖾𝗋𝖾,\n\n📌 <u>𝖸𝗈𝗎'𝗋𝖾 𝗇𝗈𝗍 𝗏𝖾𝗋𝗂𝖿𝗂𝖾𝖽 𝗍𝗈𝖽𝖺𝗒, 𝗉𝗅𝖾𝖺𝗌𝖾 𝗏𝖾𝗋𝗂𝖿𝗒 𝖺𝗇𝖽 𝗀𝖾𝗍 𝗎𝗇𝗅𝗂𝗆𝗂𝗍𝖾𝖽 𝖺𝖼𝖼𝖾𝗌𝗌 𝗍𝗂𝗅𝗅 𝗇𝖾𝗑𝗍 𝗏𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇.</u>.</b>",
            protect_content=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return
    msg = await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False,
        reply_markup=InlineKeyboardMarkup(
            [
             [
              InlineKeyboardButton('🚀 𝗙𝗮𝘀𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 / 𝗪𝗮𝘁𝗰𝗵 𝗢𝗻𝗹𝗶𝗻𝗲 🧿', callback_data=f'generate_stream_link:{file_id}'),
             ],
             [
              InlineKeyboardButton('📌 𝗝𝗼𝗶𝗻 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 📌', url=f'https://t.me/+QgSl55NlTiI0NDhl') #Don't change anything without contacting me @LazyDeveloperr
             ]
            ]
        )
    )
    btn = [[
        InlineKeyboardButton("❗ 𝗚𝗲𝘁 𝗙𝗶𝗹𝗲 𝗔𝗴𝗮𝗶𝗻 ❗", callback_data=f'delfile#{file_id}')
    ]]
    k = await client.send_message(chat_id = message.from_user.id, text=f"<b>❗️ <u>𝖨𝗆𝗉𝗈𝗋𝗍𝖺𝗇𝗍</u> ❗️</b>\n\n<b>𝖳𝗁𝗂𝗌 𝖵𝗂𝖽𝖾𝗈 / 𝖥𝗂𝗅𝖾 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗂𝗇</b> <b><u>10 𝖬𝗂𝗇𝗎𝗍𝖾𝗌</u> </b><b>(𝖣𝗎𝖾 𝗍𝗈 𝖢𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝖨𝗌𝗌𝗎𝖾𝗌).</b>\n\n<b><i>📌 𝖯𝗅𝖾𝖺𝗌𝖾 𝖥𝗈𝗋𝗐𝖺𝗋𝖽 𝗍𝗁𝗂𝗌 𝖵𝗂𝖽𝖾𝗈 / 𝖥𝗂𝗅𝖾 𝗍𝗈 𝗦𝗮𝘃𝗲𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝖺𝗇𝖽 𝖲𝗍𝖺𝗋𝗍 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝗍𝗁𝖾𝗋𝖾.</i></b>")
    await asyncio.sleep(600)
    await msg.delete()
    await k.edit_text("<b>𝖸𝗈𝗎𝗋 𝖵𝗂𝖽𝖾𝗈 / 𝖥𝗂𝗅𝖾 𝗂𝗌 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽!!\n\n𝖢𝗅𝗂𝖼𝗄 𝖻𝖾𝗅𝗈𝗐 𝖻𝗎𝗍𝗍𝗈𝗇 𝗍𝗈 𝗀𝖾𝗍 𝗒𝗈𝗎𝗋 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖵𝗂𝖽𝖾𝗈 / 𝖥𝗂𝗅𝖾 𝖠𝗀𝖺𝗂𝗇 👇</b>",reply_markup=InlineKeyboardMarkup(btn))
    return  

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("𝖴𝗇𝖾𝗑𝗉𝖾𝖼𝗍𝖾𝖽 𝗍𝗒𝗉𝖾 𝗈𝖿 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌.")

    text = '📑 **𝖨𝗇𝖽𝖾𝗑𝖾𝖽 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌 / 𝖦𝗋𝗈𝗎𝗉𝗌 𝖫𝗂𝗌𝗍:**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**𝖳𝗈𝗍𝖺𝗅:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TELEGRAM BOT.LOG')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("𝖯𝗋𝗈𝖼𝖾𝗌𝗌𝗂𝗇𝗀...⏳", quote=True)
    else:
        await message.reply('𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝗍𝗁𝖾 𝖿𝗂𝗅𝖾/𝗏𝗂𝖽𝖾𝗈 𝗐𝗂𝗍𝗁 /delete 𝗐𝗁𝗂𝖼𝗁 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾.', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('𝖳𝗁𝗂𝗌 𝗂𝗌 𝗇𝗈𝗍 𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝖿𝗂𝗅𝖾 𝖿𝗈𝗋𝗆𝖺𝗍.')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('𝖦𝗂𝗏𝖾𝗇 𝖥𝗂𝗅𝖾/𝖵𝗂𝖽𝖾𝗈 𝗂𝗌 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 ✅')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('𝖦𝗂𝗏𝖾𝗇 𝖥𝗂𝗅𝖾/𝖵𝗂𝖽𝖾𝗈 𝗂𝗌 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 ✅')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('𝖦𝗂𝗏𝖾𝗇 𝖥𝗂𝗅𝖾/𝖵𝗂𝖽𝖾𝗈 𝗂𝗌 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 ✅')
            else:
                await msg.edit('𝖥𝗂𝗅𝖾 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝗍𝗁𝖾 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾 ❌')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        '𝖳𝗁𝗂𝗌 𝗐𝗂𝗅𝗅 𝖽𝖾𝗅𝖾𝗍𝖾 𝖺𝗅𝗅 𝗍𝗁𝖾 𝗂𝗇𝖽𝖾𝗑𝖾𝖽 𝖿𝗂𝗅𝖾𝗌!\n𝖣𝗈 𝗒𝗈𝗎 𝗌𝗍𝗂𝗅𝗅 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖼𝗈𝗇𝗍𝗂𝗇𝗎𝖾?',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⚠️ 𝗬𝗲𝘀 𝗖𝗼𝗻𝘁𝗶𝗻𝘂𝗲 ⚠️", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ 𝗡𝗼 𝗔𝗯𝗼𝗿𝘁 ❌", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer('𝖬𝖺𝗂𝗇𝗍𝖺𝗂𝗇𝖾𝖽 𝖡𝗒 @𝖦𝖺𝗆𝖾𝗋𝖡𝗁𝖺𝗂02')
    await message.message.edit('𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖠𝗅𝗅 𝖨𝗇𝖽𝖾𝗑𝖾𝖽 𝖥𝗂𝗅𝖾𝗌 ✅')


@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ.\nᴜꜱᴇ /connect {message.chat.id} ɪɴ ᴘᴍ.")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("ᴍᴀᴋᴇ ꜱᴜʀᴇ ɪ'ᴍ ᴘʀᴇꜱᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("ɪ'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘ !", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return
    
    settings = await get_settings(grp_id)

    try:
        if settings['max_btn']:
            settings = await get_settings(grp_id)
    except KeyError:
        await save_group_settings(grp_id, 'max_btn', False)
        settings = await get_settings(grp_id)
    if 'is_shortlink' not in settings.keys():
        await save_group_settings(grp_id, 'is_shortlink', False)
    else:
        pass

    if settings is not None:
        buttons = [        
                [
                InlineKeyboardButton(
                    'ʀᴇꜱᴜʟᴛ ᴘᴀɢᴇ',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'ʙᴜᴛᴛᴏɴ' if settings["button"] else 'ᴛᴇxᴛ',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'ꜰɪʟᴇ ꜱᴇɴᴅ ᴍᴏᴅᴇ',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'ꜱᴛᴀʀᴛ' if settings["botpm"] else 'ᴀᴜᴛᴏ',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'ꜰɪʟᴇ ꜱᴇᴄᴜʀᴇ',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'ᴇɴᴀʙʟᴇ' if settings["file_secure"] else 'ᴅɪꜱᴀʙʟᴇ',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'ɪᴍᴅʙ ᴘᴏꜱᴛᴇʀ',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'ᴇɴᴀʙʟᴇ' if settings["imdb"] else 'ᴅɪꜱᴀʙʟᴇ',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'ꜱᴘᴇʟʟ ᴄʜᴇᴄᴋ',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'ᴇɴᴀʙʟᴇ' if settings["spell_check"] else 'ᴅɪꜱᴀʙʟᴇ',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'ᴡᴇʟᴄᴏᴍᴇ ᴍꜱɢ',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'ᴇɴᴀʙʟᴇ' if settings["welcome"] else 'ᴅɪꜱᴀʙʟᴇ',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'ᴇɴᴀʙʟᴇ' if settings["auto_delete"] else 'ᴅɪꜱᴀʙʟᴇ',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ',
                    callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'ᴇɴᴀʙʟᴇ' if settings["auto_ffilter"] else 'ᴅɪꜱᴀʙʟᴇ',
                    callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'ᴍᴀx ʙᴜᴛᴛᴏɴꜱ',
                    callback_data=f'setgs#max_btn#{settings["max_btn"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '10' if settings["max_btn"] else f'{MAX_B_TN}',
                    callback_data=f'setgs#max_btn#{settings["max_btn"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'ꜱʜᴏʀᴛʟɪɴᴋ',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'ᴇɴᴀʙʟᴇ' if settings["is_shortlink"] else 'ᴅɪꜱᴀʙʟᴇ',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton('⇋ ᴄʟᴏꜱᴇ ꜱᴇᴛᴛɪɴɢꜱ ᴍᴇɴᴜ ⇋', 
                                     callback_data='close_data'
                                     )
            ]
        ]
        

        btn = [[
                InlineKeyboardButton("👤 ᴏᴘᴇɴ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ 👤", callback_data=f"opnsetpm#{grp_id}")
              ],[
                InlineKeyboardButton("👥 ᴏᴘᴇɴ ʜᴇʀᴇ 👥", callback_data=f"opnsetgrp#{grp_id}")
              ]]

        reply_markup = InlineKeyboardMarkup(buttons)
        if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            await message.reply_text(
                text="<b>ᴡʜᴇʀᴇ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴏᴘᴇɴ ꜱᴇᴛᴛɪɴɢꜱ ᴍᴇɴᴜ ? ⚙️</b>",
                reply_markup=InlineKeyboardMarkup(btn),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )
        else:
            await message.reply_text(
                text=f"<b>ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ꜱᴇᴛᴛɪɴɢꜱ ꜰᴏʀ {title} ᴀꜱ ʏᴏᴜ ᴡɪꜱʜ ⚙</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )



@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    sts = await message.reply("ᴄʜᴇᴄᴋɪɴɢ ᴛᴇᴍᴘʟᴀᴛᴇ...")
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ.\nᴜꜱᴇ /connect {message.chat.id} ɪɴ ᴘᴍ.")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("ᴍᴀᴋᴇ ꜱᴜʀᴇ ɪ'ᴍ ᴘʀᴇꜱᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("ɪ'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘ !", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("ɴᴏ ɪɴᴘᴜᴛ !")
    template = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', template)
    await sts.edit(f"✅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴛᴇᴍᴘʟᴀᴛᴇ ꜰᴏʀ <code>{title}</code> ᴛᴏ\n\n{template}")


@Client.on_message((filters.command(["request", "Request"]) | filters.regex("#request") | filters.regex("#Request")) & filters.group)
async def requests(bot, message):
    if REQST_CHANNEL is None or SUPPORT_CHAT_ID is None: return # Must add REQST_CHANNEL and SUPPORT_CHAT_ID to use this feature
    if message.reply_to_message and SUPPORT_CHAT_ID == message.chat.id:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.reply_to_message.text
        try:
            if REQST_CHANNEL is not None:
                btn = [[
                        InlineKeyboardButton('ᴠɪᴇᴡ ʀᴇǫᴜᴇꜱᴛ', url=f"{message.reply_to_message.link}"),
                        InlineKeyboardButton('ꜱʜᴏᴡ ᴏᴘᴛɪᴏɴꜱ', callback_data=f'show_option#{reporter}')
                      ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>📝 ʀᴇǫᴜᴇꜱᴛ : <u>{content}</u>\n\n📚 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ : {mention}\n📖 ʀᴇᴘᴏʀᴛᴇʀ ɪᴅ : {reporter}\n\n©️ AllMoviesLink™</b>", reply_markup=InlineKeyboardMarkup(btn))
                success = True
            elif len(content) >= 3:
                for admin in ADMINS:
                    btn = [[
                        InlineKeyboardButton('ᴠɪᴇᴡ ʀᴇǫᴜᴇꜱᴛ', url=f"{message.reply_to_message.link}"),
                        InlineKeyboardButton('ꜱʜᴏᴡ ᴏᴘᴛɪᴏɴꜱ', callback_data=f'show_option#{reporter}')
                      ]]
                    reported_post = await bot.send_message(chat_id=admin, text=f"<b>📝 ʀᴇǫᴜᴇꜱᴛ : <u>{content}</u>\n\n📚 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ : {mention}\n📖 ʀᴇᴘᴏʀᴛᴇʀ ɪᴅ : {reporter}\n\n©️ AllMoviesLink™</b>", reply_markup=InlineKeyboardMarkup(btn))
                    success = True
            else:
                if len(content) < 3:
                    await message.reply_text("<b>ʏᴏᴜ ᴍᴜꜱᴛ ᴛʏᴘᴇ ᴀʙᴏᴜᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ [ᴍɪɴɪᴍᴜᴍ 3 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ]. ʀᴇǫᴜᴇꜱᴛꜱ ᴄᴀɴ'ᴛ ʙᴇ ᴇᴍᴘᴛʏ.</b>")
            if len(content) < 3:
                success = False
        except Exception as e:
            await message.reply_text(f"Error: {e}")
            pass
        
    elif SUPPORT_CHAT_ID == message.chat.id:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.text
        keywords = ["#request", "/request", "#Request", "/Request"]
        for keyword in keywords:
            if keyword in content:
                content = content.replace(keyword, "")
        try:
            if REQST_CHANNEL is not None and len(content) >= 3:
                btn = [[
                        InlineKeyboardButton('ᴠɪᴇᴡ ʀᴇǫᴜᴇꜱᴛ', url=f"{message.link}"),
                        InlineKeyboardButton('ꜱʜᴏᴡ ᴏᴘᴛɪᴏɴꜱ', callback_data=f'show_option#{reporter}')
                      ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>📝 ʀᴇǫᴜᴇꜱᴛ : <u>{content}</u>\n\n📚 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ : {mention}\n📖 ʀᴇᴘᴏʀᴛᴇʀ ɪᴅ : {reporter}\n\n©️ AllMoviesLink™</b>", reply_markup=InlineKeyboardMarkup(btn))
                success = True
            elif len(content) >= 3:
                for admin in ADMINS:
                    btn = [[
                        InlineKeyboardButton('ᴠɪᴇᴡ ʀᴇǫᴜᴇꜱᴛ', url=f"{message.link}"),
                        InlineKeyboardButton('ꜱʜᴏᴡ ᴏᴘᴛɪᴏɴꜱ', callback_data=f'show_option#{reporter}')
                      ]]
                    reported_post = await bot.send_message(chat_id=admin, text=f"<b>📝 ʀᴇǫᴜᴇꜱᴛ : <u>{content}</u>\n\n📚 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ : {mention}\n📖 ʀᴇᴘᴏʀᴛᴇʀ ɪᴅ : {reporter}\n\n©️ AllMoviesLink™</b>", reply_markup=InlineKeyboardMarkup(btn))
                    success = True
            else:
                if len(content) < 3:
                    await message.reply_text("<b>ʏᴏᴜ ᴍᴜꜱᴛ ᴛʏᴘᴇ ᴀʙᴏᴜᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ [ᴍɪɴɪᴍᴜᴍ 3 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ]. ʀᴇǫᴜᴇꜱᴛꜱ ᴄᴀɴ'ᴛ ʙᴇ ᴇᴍᴘᴛʏ.</b>")
            if len(content) < 3:
                success = False
        except Exception as e:
            await message.reply_text(f"Error: {e}")
            pass
     
    elif SUPPORT_CHAT_ID == message.chat.id:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.text
        keywords = ["#request", "/request", "#Request", "/Request"]
        for keyword in keywords:
            if keyword in content:
                content = content.replace(keyword, "")
        try:
            if REQST_CHANNEL is not None and len(content) >= 3:
                btn = [[
                        InlineKeyboardButton('ᴠɪᴇᴡ ʀᴇǫᴜᴇꜱᴛ', url=f"{message.link}"),
                        InlineKeyboardButton('ꜱʜᴏᴡ ᴏᴘᴛɪᴏɴꜱ', callback_data=f'show_option#{reporter}')
                      ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>📝 ʀᴇǫᴜᴇꜱᴛ : <u>{content}</u>\n\n📚 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ : {mention}\n📖 ʀᴇᴘᴏʀᴛᴇʀ ɪᴅ : {reporter}\n\n©️ AllMoviesLink™</b>", reply_markup=InlineKeyboardMarkup(btn))
                success = True
            elif len(content) >= 3:
                for admin in ADMINS:
                    btn = [[
                        InlineKeyboardButton('ᴠɪᴇᴡ ʀᴇǫᴜᴇꜱᴛ', url=f"{message.link}"),
                        InlineKeyboardButton('ꜱʜᴏᴡ ᴏᴘᴛɪᴏɴꜱ', callback_data=f'show_option#{reporter}')
                      ]]
                    reported_post = await bot.send_message(chat_id=admin, text=f"<b>📝 ʀᴇǫᴜᴇꜱᴛ : <u>{content}</u>\n\n📚 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ : {mention}\n📖 ʀᴇᴘᴏʀᴛᴇʀ ɪᴅ : {reporter}\n\n©️ AllMoviesLink™</b>", reply_markup=InlineKeyboardMarkup(btn))
                    success = True
            else:
                if len(content) < 3:
                    await message.reply_text("<b>ʏᴏᴜ ᴍᴜꜱᴛ ᴛʏᴘᴇ ᴀʙᴏᴜᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ [ᴍɪɴɪᴍᴜᴍ 3 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ]. ʀᴇǫᴜᴇꜱᴛꜱ ᴄᴀɴ'ᴛ ʙᴇ ᴇᴍᴘᴛʏ.</b>")
            if len(content) < 3:
                success = False
        except Exception as e:
            await message.reply_text(f"Error: {e}")
            pass

    else:
        success = False
    
    if success:
        '''if isinstance(REQST_CHANNEL, (int, str)):
            channels = [REQST_CHANNEL]
        elif isinstance(REQST_CHANNEL, list):
            channels = REQST_CHANNEL
        for channel in channels:
            chat = await bot.get_chat(channel)
        #chat = int(chat)'''
        link = await bot.create_chat_invite_link(int(REQST_CHANNEL))
        btn = [[
                InlineKeyboardButton('ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ', url=link.invite_link),
                InlineKeyboardButton('ᴠɪᴇᴡ ʀᴇǫᴜᴇꜱᴛ', url=f"{reported_post.link}")
              ]]
        await message.reply_text("<b>ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ! ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ ꜱᴏᴍᴇ ᴛɪᴍᴇ.\n\nᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ꜰɪʀꜱᴛ & ᴠɪᴇᴡ ʀᴇǫᴜᴇꜱᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn))
    
@Client.on_message(filters.command("send") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_id = message.text.split(" ", 1)[1]
        out = "Users Saved In DB Are:\n\n"
        success = False
        try:
            user = await bot.get_users(target_id)
            users = await db.get_all_users()
            async for usr in users:
                out += f"{usr['id']}"
                out += '\n'
            if str(user.id) in str(out):
                await message.reply_to_message.copy(int(user.id))
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇɴᴛ ᴛᴏ {user.mention}.</b>")
            else:
                await message.reply_text("<b>ᴛʜɪꜱ ᴜꜱᴇʀ ᴅɪᴅɴ'ᴛ ꜱᴛᴀʀᴛᴇᴅ ᴛʜɪꜱ ʙᴏᴛ ʏᴇᴛ !</b>")
        except Exception as e:
            await message.reply_text(f"<b>Error: {e}</b>")
    else:
        await message.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴀꜱ ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇ ᴜꜱɪɴɢ ᴛʜᴇ ᴛᴀʀɢᴇᴛ ᴄʜᴀᴛ ɪᴅ. ꜰᴏʀ ᴇɢ:  /send ᴜꜱᴇʀɪᴅ</b>")

@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))

async def deletemultiplefiles(bot, message):

    chat_type = message.chat.type

    if chat_type != enums.ChatType.PRIVATE:

        return await message.reply_text(f"<b>𝖧𝖾𝗒 {message.from_user.mention},\nᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡᴏɴ'ᴛ ᴡᴏʀᴋ ɪɴ ɢʀᴏᴜᴘꜱ !\nɪᴛ ᴏɴʟʏ ᴡᴏʀᴋꜱ ɪɴ ᴍʏ ᴘᴍ.</b>")

    else:

        pass

    try:

        keyword = message.text.split(" ", 1)[1]

    except:

        return await message.reply_text(f"<b>𝖧𝖾𝗒 {message.from_user.mention},\nɢɪᴠᴇ ᴍᴇ ᴀ ᴋᴇʏᴡᴏʀᴅ ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ꜰɪʟᴇꜱ.</b>")

    btn = [[

       InlineKeyboardButton("⚠️ 𝗬𝗲𝘀 𝗖𝗼𝗻𝘁𝗶𝗻𝘂𝗲 ⚠️", callback_data=f"killfilesdq#{keyword}")

       ],[

       InlineKeyboardButton("❌ 𝗡𝗼 𝗔𝗯𝗼𝗿𝘁 ❌", callback_data="close_data")

    ]]

    await message.reply_text(

        text="<b>ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ?\nɴᴏᴛᴇ : ᴛʜɪꜱ ᴄᴏᴜʟᴅ ʙᴇ ᴀ ᴅᴇꜱᴛʀᴜᴄᴛɪᴠᴇ ᴅᴇꜱɪᴄɪᴏɴ.</b>",

        reply_markup=InlineKeyboardMarkup(btn),

        parse_mode=enums.ParseMode.HTML

    )

@Client.on_message(filters.command("shortlink"))
async def shortlink(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ, ᴛᴜʀɴ ᴏꜰꜰ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ ᴀɴᴅ ᴛʀʏ ᴛʜɪꜱ ᴀɢᴀɪɴ ᴄᴏᴍᴍᴀɴᴅ.")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>𝖧𝖾𝗒 {message.from_user.mention}, ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋꜱ ɪɴ ɢʀᴏᴜᴘꜱ !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    data = message.text
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇꜱꜱ ᴛᴏ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ !\nᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋꜱ ꜰᴏʀ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴꜱ.</b>")
    else:
        pass
    try:
        command, shortlink_url, api = data.split(" ")
    except:
        return await message.reply_text("<b>ᴄᴏᴍᴍᴀɴᴅ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ !\nɢɪᴠᴇ ᴍᴇ ᴄᴏᴍᴍᴀɴᴅ ᴀʟᴏɴɢ ᴡɪᴛʜ ꜱʜᴏʀᴛɴᴇʀ ᴡᴇʙꜱɪᴛᴇ ᴀɴᴅ ᴀᴘɪ.\n\nꜰᴏʀᴍᴀᴛ : <code>/shortlink upshrink.com 9a0b1fe3b239b30fe65ab3e4ebeb048ca10c91c4</code>")
    reply = await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
    shortlink_url = re.sub(r"https?://?", "", shortlink_url)
    shortlink_url = re.sub(r"[:/]", "", shortlink_url)
    await save_group_settings(grpid, 'shortlink', shortlink_url)
    await save_group_settings(grpid, 'shortlink_api', api)
    await save_group_settings(grpid, 'is_shortlink', True)
    await reply.edit_text(f"<b>✅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ꜱʜᴏʀᴛʟɪɴᴋ ꜰᴏʀ <code>{title}</code>.\n\nꜱʜᴏʀᴛʟɪɴᴋ ᴡᴇʙꜱɪᴛᴇ : <code>{shortlink_url}</code>\nꜱʜᴏʀᴛʟɪɴᴋ ᴀᴘɪ : <code>{api}</code></b>")

@Client.on_message(filters.command("setshortlinkoff") & filters.user(ADMINS))
async def offshortlink(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋꜱ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘꜱ !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    await save_group_settings(grpid, 'is_shortlink', False)
    ENABLE_SHORTLINK = False
    return await message.reply_text("ꜱʜᴏʀᴛʟɪɴᴋ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅɪꜱᴀʙʟᴇᴅ.")
    
@Client.on_message(filters.command("setshortlinkon") & filters.user(ADMINS))
async def onshortlink(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋꜱ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘꜱ !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    await save_group_settings(grpid, 'is_shortlink', True)
    ENABLE_SHORTLINK = True
    return await message.reply_text("ꜱʜᴏʀᴛʟɪɴᴋ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴇɴᴀʙʟᴇᴅ.")


@Client.on_message(filters.command("shortlink_info"))
async def ginfo(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>{message.from_user.mention},\n\nᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    chat_id=message.chat.id
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
#     if 'shortlink' in settings.keys():
#         su = settings['shortlink']
#         sa = settings['shortlink_api']
#     else:
#         return await message.reply_text("<b>Shortener Url Not Connected\n\nYou can Connect Using /shortlink command</b>")
#     if 'tutorial' in settings.keys():
#         st = settings['tutorial']
#     else:
#         return await message.reply_text("<b>Tutorial Link Not Connected\n\nYou can Connect Using /set_tutorial command</b>")
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>ᴏɴʟʏ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴏʀ ᴀᴅᴍɪɴ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ !</b>")
    else:
        settings = await get_settings(chat_id) #fetching settings for group
        if 'shortlink' in settings.keys() and 'tutorial' in settings.keys():
            su = settings['shortlink']
            sa = settings['shortlink_api']
            st = settings['tutorial']
            return await message.reply_text(f"<b><u>ᴄᴜʀʀᴇɴᴛ  ꜱᴛᴀᴛᴜꜱ<u> 📊\n\nᴡᴇʙꜱɪᴛᴇ : <code>{su}</code>\n\nᴀᴘɪ : <code>{sa}</code>\n\nᴛᴜᴛᴏʀɪᴀʟ : {st}</b>", disable_web_page_preview=True)
        elif 'shortlink' in settings.keys() and 'tutorial' not in settings.keys():
            su = settings['shortlink']
            sa = settings['shortlink_api']
            return await message.reply_text(f"<b><u>ᴄᴜʀʀᴇɴᴛ  ꜱᴛᴀᴛᴜꜱ<u> 📊\n\nᴡᴇʙꜱɪᴛᴇ : <code>{su}</code>\n\nᴀᴘɪ : <code>{sa}</code>\n\nᴜꜱᴇ /set_tutorial ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ꜱᴇᴛ ʏᴏᴜʀ ᴛᴜᴛᴏʀɪᴀʟ.")
        elif 'shortlink' not in settings.keys() and 'tutorial' in settings.keys():
            st = settings['tutorial']
            return await message.reply_text(f"<b>ᴛᴜᴛᴏʀɪᴀʟ : <code>{st}</code>\n\nᴜꜱᴇ  /shortlink  ᴄᴏᴍᴍᴀɴᴅ  ᴛᴏ  ᴄᴏɴɴᴇᴄᴛ  ʏᴏᴜʀ  ꜱʜᴏʀᴛɴᴇʀ</b>")
        else:
            return await message.reply_text("ꜱʜᴏʀᴛɴᴇʀ ᴀɴᴅ ᴛᴜᴛᴏʀɪᴀʟ ᴀʀᴇ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ.\n\nᴄʜᴇᴄᴋ /set_tutorial  ᴀɴᴅ  /shortlink  ᴄᴏᴍᴍᴀɴᴅ.")

@Client.on_message(filters.command("set_tutorial"))
async def settutorial(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ, ᴛᴜʀɴ ᴏꜰꜰ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋꜱ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘꜱ !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    if len(message.command) == 1:
        return await message.reply("<b>ɢɪᴠᴇ ᴍᴇ ᴀ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.\n\nᴜꜱᴀɢᴇ : /set_tutorial <code>https://t.me/link</code></b>")
    elif len(message.command) == 2:
        reply = await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
        tutorial = message.command[1]
        await save_group_settings(grpid, 'tutorial', tutorial)
        await save_group_settings(grpid, 'is_tutorial', True)
        await reply.edit_text(f"<b>✅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴜᴛᴏʀɪᴀʟ\n\nʏᴏᴜʀ ɢʀᴏᴜᴘ : {title}\n\nʏᴏᴜʀ ᴛᴜᴛᴏʀɪᴀʟ : <code>{tutorial}</code></b>")
    else:
        return await message.reply("<b>ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ɪɴᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ !\nᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ : /set_tutorial <code>https://t.me/link</code></b>")

@Client.on_message(filters.command("remove_tutorial"))
async def removetutorial(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ, ᴛᴜʀɴ ᴏꜰꜰ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋꜱ ɪɴ ɢʀᴏᴜᴘꜱ !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    reply = await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
    await save_group_settings(grpid, 'is_tutorial', False)
    await reply.edit_text(f"<b>ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ ✅</b>")

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def stop_button(bot, message):
    msg = await bot.send_message(text="<b><i>ʙᴏᴛ ɪꜱ ʀᴇꜱᴛᴀʀᴛɪɴɢ</i></b>", chat_id=message.chat.id)       
    await asyncio.sleep(3)
    await msg.edit("<b><i><u>ʙᴏᴛ ɪꜱ ʀᴇꜱᴛᴀʀᴛᴇᴅ</u> ✅</i></b>")
    os.execl(sys.executable, sys.executable, *sys.argv)
