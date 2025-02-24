from pyrogram import Client, filters
from utils import temp
from pyrogram.types import Message
from database.users_chats_db import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import SUPPORT_CHAT

async def banned_users(_, client, message: Message):
    return (
        message.from_user is not None or not message.sender_chat
    ) and message.from_user.id in temp.BANNED_USERS

banned_user = filters.create(banned_users)

async def disabled_chat(_, client, message: Message):
    return message.chat.id in temp.BANNED_CHATS

disabled_group=filters.create(disabled_chat)


@Client.on_message(filters.private & banned_user & filters.incoming)
async def ban_reply(bot, message):
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply(f'𝖲𝗈𝗋𝗋𝗒 𝖣𝗎𝖽𝖾, 𝖸𝗈𝗎 𝖺𝗋𝖾 𝖡𝖺𝗇𝗇𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗆𝖾. \n𝖡𝖺𝗇 𝖱𝖾𝖺𝗌𝗈𝗇: {ban["ban_reason"]}')

@Client.on_message(filters.group & disabled_group & filters.incoming)
async def grp_bd(bot, message):
    buttons = [[
        InlineKeyboardButton('𝗦𝘂𝗽𝗽𝗼𝗿𝘁/𝗔𝗱𝗺𝗶𝗻', url=f'https://t.me/GamerBhai02')
    ]]
    reply_markup=InlineKeyboardMarkup(buttons)
    vazha = await db.get_chat(message.chat.id)
    k = await message.reply(
        text=f"𝗖𝗛𝗔𝗧 𝗡𝗢𝗧 𝗔𝗟𝗟𝗢𝗪𝗘𝗗 🐞\n\n𝖬𝗒 𝖺𝖽𝗆𝗂𝗇𝗌 𝗁𝖺𝗌 𝗋𝖾𝗌𝗍𝗋𝗂𝖼𝗍𝖾𝖽 𝗆𝖾 𝖿𝗋𝗈𝗆 𝗐𝗈𝗋𝗄𝗂𝗇𝗀 𝗁𝖾𝗋𝖾! 𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝗄𝗇𝗈𝗐 𝗆𝗈𝗋𝖾 𝖺𝖻𝗈𝗎𝗍 𝗂𝗍 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗌𝗎𝗉𝗉𝗈𝗋𝗍..\n𝖱𝖾𝖺𝗌𝗈𝗇: <code>{vazha['reason']}</code>.",
        reply_markup=reply_markup)
    try:
        await k.pin()
    except:
        pass
    await bot.leave_chat(message.chat.id)
