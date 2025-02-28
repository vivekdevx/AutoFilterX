from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS, MELCOW_VID, CHNL_LNK, GRP_LNK
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp, get_settings
from Script import script
from pyrogram.errors import ChatAdminRequired
import asyncio 

"""-----------------------------------------https://t.me/AllMoviesLinkBot--------------------------------------"""

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            # Inspired from a boat of a banana tree
            buttons = [[
                InlineKeyboardButton('📌 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍 📌', url=f'https://t.me/GamerBhai02')
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>𝖢𝗁𝖺𝗍 𝗇𝗈𝗍 𝖺𝗅𝗅𝗈𝗐𝖾𝖽 🐞\n\n𝖬𝗒 𝖺𝖽𝗆𝗂𝗇 𝗁𝖺𝗌 𝗋𝖾𝗌𝗍𝗋𝗂𝖼𝗍𝖾𝖽 𝗆𝖾 𝖿𝗋𝗈𝗆 𝗐𝗈𝗋𝗄𝗂𝗇𝗀 𝗁𝖾𝗋𝖾! 𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝗄𝗇𝗈𝗐 𝗆𝗈𝗋𝖾 𝖺𝖻𝗈𝗎𝗍 𝗂𝗍 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍.</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
                    InlineKeyboardButton("🍁 𝖧𝗈𝗐 𝗍𝗈 𝗎𝗌𝖾 🍁", url="https://t.me/AllMoviesLinkBot?start=help")
                  ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b>›› 𝖳𝗁𝖺𝗇𝗄𝗌 𝖿𝗈𝗋 𝖺𝖽𝖽𝗂𝗇𝗀 𝗆𝖾 𝗂𝗇 {message.chat.title} \n›› 𝖣𝗈𝗇'𝗍 𝖿𝗈𝗋𝗀𝖾𝗍 𝗍𝗈 𝗆𝖺𝗄𝖾 𝗆𝖾 𝖠𝖽𝗆𝗂𝗇.\n›› 𝖨𝖿 𝖺𝗇𝗒 𝖽𝗈𝗎𝖻𝗍𝗌 𝖺𝖻𝗈𝗎𝗍 𝗎𝗌𝗂𝗇𝗀 𝗆𝖾 𝖼𝗅𝗂𝖼𝗄 𝖻𝖾𝗅𝗈𝗐 𝖻𝗎𝗍𝗍𝗈𝗇 👇</b>",
            reply_markup=reply_markup)
    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            for u in message.new_chat_members:
                if (temp.MELCOW).get('welcome') is not None:
                    try:
                        await (temp.MELCOW['welcome']).delete()
                    except:
                        pass
                temp.MELCOW['welcome'] = await message.reply_video(
                                                 video=(MELCOW_VID),
                                                 caption=(script.MELCOW_ENG.format(u.mention, message.chat.title)),
                                                 reply_markup=InlineKeyboardMarkup(
                                                                         [[
                                                                           InlineKeyboardButton("📌 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍 📌", url=f'https://t.me/GamerBhai02')
                                                                         ]]
                                                 ),
                                                 parse_mode=enums.ParseMode.HTML
                )
                
        if settings["auto_delete"]:
            await asyncio.sleep(600)
            await (temp.MELCOW['welcome']).delete()
                
               



@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('𝖦𝗂𝗏𝖾 𝗆𝖾 𝖺 𝖼𝗁𝖺𝗍 𝗂𝖽')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
                  InlineKeyboardButton("📌 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍 📌", url="https://t.me/GamerBhai02")
                  ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>𝖧𝖾𝗅𝗅𝗈 𝖥𝗋𝗂𝖾𝗇𝖽𝗌, \n𝖬𝗒 𝖺𝖽𝗆𝗂𝗇 𝗁𝖺𝗌 𝗍𝗈𝗅𝖽 𝗆𝖾 𝗍𝗈 𝗅𝖾𝖺𝗏𝖾 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉, 𝗌𝗈 𝗂 𝗁𝖺𝗏𝖾 𝗍𝗈 𝗀𝗈!/n𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖺𝖽𝖽 𝗆𝖾 𝖺𝗀𝖺𝗂𝗇 𝗍𝗁𝖾𝗇 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍.</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"𝗅𝖾𝖿𝗍 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍 `{chat}`")
    except Exception as e:
        await message.reply(f'𝖤𝗋𝗋𝗈𝗋 - {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('𝖦𝗂𝗏𝖾 𝗆𝖾 𝖺 𝖼𝗁𝖺𝗍 𝗂𝖽')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('𝖦𝗂𝗏𝖾 𝖬𝖾 𝖠 𝖵𝖺𝗅𝗂𝖽 𝖢𝗁𝖺𝗍 𝖨𝖣')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("𝖢𝗁𝖺𝗍 𝖭𝗈𝗍 𝖥𝗈𝗎𝗇𝖽 𝖨𝗇 𝖣𝖡")
    if cha_t['is_disabled']:
        return await message.reply(f"𝖳𝗁𝗂𝗌 𝖼𝗁𝖺𝗍 𝗂𝗌 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝖽𝗂𝗌𝖺𝖻𝗅𝖾𝖽:\n𝖱𝖾𝖺𝗌𝗈𝗇-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('𝖢𝗁𝖺𝗍 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝖽')
    try:
        buttons = [[
            InlineKeyboardButton('📌 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍 📌', url=f'https://t.me/GamerBhai02')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_, 
            text=f'<b>𝖧𝖾𝗅𝗅𝗈 𝖥𝗋𝗂𝖾𝗇𝖽𝗌, \n𝖬𝗒 𝖺𝖽𝗆𝗂𝗇 𝗁𝖺𝗌 𝗍𝗈𝗅𝖽 𝗆𝖾 𝗍𝗈 𝗅𝖾𝖺𝗏𝖾 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉, 𝗌𝗈 𝗂 𝗁𝖺𝗏𝖾 𝗍𝗈 𝗀𝗈! \n𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖺𝖽𝖽 𝗆𝖾 𝖺𝗀𝖺𝗂𝗇 𝗍𝗁𝖾𝗇 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍.</b> \n𝖱𝖾𝖺𝗌𝗈𝗇: <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"𝖤𝗋𝗋𝗈𝗋 - {e}")


@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('𝖦𝗂𝗏𝖾 𝗆𝖾 𝖺 𝖼𝗁𝖺𝗍 𝗂𝖽')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('𝖦𝗂𝗏𝖾 𝖬𝖾 𝖠 𝖵𝖺𝗅𝗂𝖽 𝖢𝗁𝖺𝗍 𝖨𝖣')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("𝖢𝗁𝖺𝗍 𝖭𝗈𝗍 𝖥𝗈𝗎𝗇𝖽 𝖨𝗇 𝖣𝖡!")
    if not sts.get('is_disabled'):
        return await message.reply('𝖳𝗁𝗂𝗌 𝖼𝗁𝖺𝗍 𝗂𝗌 𝗇𝗈𝗍 𝗒𝖾𝗍 𝖽𝗂𝗌𝖺𝖻𝗅𝖾𝖽.')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("𝖢𝗁𝖺𝗍 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗋𝖾-𝖾𝗇𝖺𝖻𝗅𝖾𝖽")


@Client.on_message(filters.command('stats') & filters.incoming)
async def get_ststs(bot, message):
    rju = await message.reply('𝖥𝖾𝗍𝖼𝗁𝗂𝗇𝗀 𝗌𝗍𝖺𝗍𝗌..')
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await rju.edit(script.STATUS_TXT.format(files, total_users, totl_chats, size, free))


@Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('𝖦𝗂𝗏𝖾 𝗆𝖾 𝖺 𝖼𝗁𝖺𝗍 𝗂𝖽')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('𝖦𝗂𝗏𝖾 𝖬𝖾 𝖠 𝖵𝖺𝗅𝗂𝖽 𝖢𝗁𝖺𝗍 𝖨𝖣')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("𝖨𝗇𝗏𝗂𝗍𝖾 𝖫𝗂𝗇𝗄 𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝗂𝗈𝗇 𝖥𝖺𝗂𝗅𝖾𝖽, 𝖨 𝖺𝗆 𝖭𝗈𝗍 𝖧𝖺𝗏𝗂𝗇𝗀 𝖲𝗎𝖿𝖿𝗂𝖼𝗂𝖾𝗇𝗍 𝖱𝗂𝗀𝗁𝗍𝗌")
    except Exception as e:
        return await message.reply(f'𝖤𝗋𝗋𝗈𝗋 {e}')
    await message.reply(f'𝖧𝖾𝗋𝖾 𝗂𝗌 𝗒𝗈𝗎𝗋 𝖨𝗇𝗏𝗂𝗍𝖾 𝖫𝗂𝗇𝗄 {link.invite_link}')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    # https://t.me/GetTGLink/4185
    if len(message.command) == 1:
        return await message.reply('𝖦𝗂𝗏𝖾 𝗆𝖾 𝖺 𝗎𝗌𝖾𝗋 𝗂𝖽 / 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("𝖳𝗁𝗂𝗌 𝗂𝗌 𝖺𝗇 𝗂𝗇𝗏𝖺𝗅𝗂𝖽 𝗎𝗌𝖾𝗋, 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖨 𝗁𝖺𝗏𝖾 𝗆𝖾𝗍 𝗁𝗂𝗆 𝖻𝖾𝖿𝗈𝗋𝖾.")
    except IndexError:
        return await message.reply("𝖳𝗁𝗂𝗌 𝗆𝗂𝗀𝗁𝗍 𝖻𝖾 𝖺 𝖼𝗁𝖺𝗇𝗇𝖾𝗅, 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗂𝗍𝗌 𝖺 𝗎𝗌𝖾𝗋.")
    except Exception as e:
        return await message.reply(f'𝖤𝗋𝗋𝗈𝗋 - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} 𝗂𝗌 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝖻𝖺𝗇𝗇𝖾𝖽\n𝖱𝖾𝖺𝗌𝗈𝗇: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖻𝖺𝗇𝗇𝖾𝖽 {k.mention}")


    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('𝖦𝗂𝗏𝖾 𝗆𝖾 𝖺 𝗎𝗌𝖾𝗋 𝗂𝖽 / 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("𝖳𝗁𝗂𝗌 𝗂𝗌 𝖺𝗇 𝗂𝗇𝗏𝖺𝗅𝗂𝖽 𝗎𝗌𝖾𝗋, 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗂 𝗁𝖺𝗏𝖾 𝗆𝖾𝗍 𝗁𝗂𝗆 𝖻𝖾𝖿𝗈𝗋𝖾.")
    except IndexError:
        return await message.reply("𝖳𝗁𝗂𝗌 𝗆𝗂𝗀𝗁𝗍 𝖻𝖾 𝖺 𝖼𝗁𝖺𝗇𝗇𝖾𝗅, 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗂𝗍𝗌 𝖺 𝗎𝗌𝖾𝗋.")
    except Exception as e:
        return await message.reply(f'𝖤𝗋𝗋𝗈𝗋 - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} 𝗂𝗌 𝗇𝗈𝗍 𝗒𝖾𝗍 𝖻𝖺𝗇𝗇𝖾𝖽.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗎𝗇𝖻𝖺𝗇𝗇𝖾𝖽 {k.mention}")


    
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    # https://t.me/GetTGLink/4184
    raju = await message.reply('𝖦𝖾𝗍𝗍𝗂𝗇𝗀 𝖫𝗂𝗌𝗍 𝖮𝖿 𝖴𝗌𝖾𝗋𝗌')
    users = await db.get_all_users()
    out = "𝖴𝗌𝖾𝗋𝗌 𝖲𝖺𝗏𝖾𝖽 𝖨𝗇 𝖣𝖡 𝖠𝗋𝖾:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="𝖫𝗂𝗌𝗍 𝖮𝖿 𝖴𝗌𝖾𝗋𝗌")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('𝖦𝖾𝗍𝗍𝗂𝗇𝗀 𝖫𝗂𝗌𝗍 𝖮𝖿 𝖼𝗁𝖺𝗍𝗌')
    chats = await db.get_all_chats()
    out = "𝖢𝗁𝖺𝗍𝗌 𝖲𝖺𝗏𝖾𝖽 𝖨𝗇 𝖣𝖡 𝖠𝗋𝖾:\n\n"
    async for chat in chats:
        out += f"**𝖳𝗂𝗍𝗅𝖾:** `{chat['title']}`\n**- 𝖨𝖣:** `{chat['id']}`"
        if chat['chat_status']['is_disabled']:
            out += '( Disabled Chat )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="𝖫𝗂𝗌𝗍 𝖮𝖿 𝖢𝗁𝖺𝗍𝗌")
