import logging
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import ADMINS
from info import INDEX_REQ_CHANNEL as LOG_CHANNEL
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import temp
import re
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()


@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝗂𝗇𝗀 𝖨𝗇𝖽𝖾𝗑𝗂𝗇𝗀")
    _, raju, chat, lst_msg_id, from_user = query.data.split("#")
    if raju == 'reject':
        await query.message.delete()
        await bot.send_message(int(from_user),
                               f'𝖸𝗈𝗎𝗋 𝖲𝗎𝖻𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝖿𝗈𝗋 𝗂𝗇𝖽𝖾𝗑𝗂𝗇𝗀 {chat} 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖽𝖾𝖼𝗅𝗂𝗇𝖾𝖽 𝖻𝗒 𝗈𝗎𝗋 𝗆𝗈𝖽𝖾𝗋𝖺𝗍𝗈𝗋𝗌.',
                               reply_to_message_id=int(lst_msg_id))
        return

    if lock.locked():
        return await query.answer('𝖶𝖺𝗂𝗍 𝗎𝗇𝗍𝗂𝗅 𝗉𝗋𝖾𝗏𝗂𝗈𝗎𝗌 𝗉𝗋𝗈𝖼𝖾𝗌𝗌 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾.', show_alert=True)
    msg = query.message

    await query.answer('𝖯𝗋𝗈𝖼𝖾𝗌𝗌𝗂𝗇𝗀...⏳', show_alert=True)
    if int(from_user) not in ADMINS:
        await bot.send_message(int(from_user),
                               f'𝖸𝗈𝗎𝗋 𝖲𝗎𝖻𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝖿𝗈𝗋 𝗂𝗇𝖽𝖾𝗑𝗂𝗇𝗀 {chat} 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖺𝖼𝖼𝖾𝗉𝗍𝖾𝖽 𝖻𝗒 𝗈𝗎𝗋 𝗆𝗈𝖽𝖾𝗋𝖺𝗍𝗈𝗋𝗌 𝖺𝗇𝖽 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖺𝖽𝖽𝖾𝖽 𝗌𝗈𝗈𝗇.',
                               reply_to_message_id=int(lst_msg_id))
    await msg.edit(
        "𝖲𝗍𝖺𝗋𝗍𝗂𝗇𝗀 𝖨𝗇𝖽𝖾𝗑𝗂𝗇𝗀",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('𝗖𝗮𝗻𝗰𝗲𝗹', callback_data='index_cancel')]]
        )
    )
    try:
        chat = int(chat)
    except:
        chat = chat
    await index_files_to_db(int(lst_msg_id), chat, msg, bot)


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming)
async def send_for_index(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗅𝗂𝗇𝗄')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return
    try:
        await bot.get_chat(chat_id)
    except ChannelInvalid:
        return await message.reply('𝖳𝗁𝗂𝗌 𝗆𝖺𝗒 𝖻𝖾 𝖺 𝗉𝗋𝗂𝗏𝖺𝗍𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 / 𝗀𝗋𝗈𝗎𝗉. 𝖬𝖺𝗄𝖾 𝗆𝖾 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗈𝗏𝖾𝗋 𝗍𝗁𝖾𝗋𝖾 𝗍𝗈 𝗂𝗇𝖽𝖾𝗑 𝗍𝗁𝖾 𝖿𝗂𝗅𝖾𝗌.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖫𝗂𝗇𝗄 𝗌𝗉𝖾𝖼𝗂𝖿𝗂𝖾𝖽.')
    except Exception as e:
        logger.exception(e)
        return await message.reply(f'𝖤𝗋𝗋𝗈𝗋𝗌 - {e}')
    try:
        k = await bot.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('𝖬𝖺𝗄𝖾 𝖲𝗎𝗋𝖾 𝖳𝗁𝖺𝗍 𝖨 𝖺𝗆 𝖠𝗇 𝖠𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝖾 𝖢𝗁𝖺𝗇𝗇𝖾𝗅, 𝗂𝖿 𝗍𝗁𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝗌 𝗉𝗋𝗂𝗏𝖺𝗍𝖾.')
    if k.empty:
        return await message.reply('𝖳𝗁𝗂𝗌 𝗆𝖺𝗒 𝖻𝖾 𝖺 𝗀𝗋𝗈𝗎𝗉 𝖺𝗇𝖽 𝗂 𝖺𝗆 𝗇𝗈𝗍 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗈𝖿 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉.')

    if message.from_user.id in ADMINS:
        buttons = [
            [
                InlineKeyboardButton('𝗬𝗘𝗦',
                                     callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
            ],
            [
                InlineKeyboardButton('𝗖𝗟𝗢𝗦𝗘', callback_data='close_data'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply(
            f'𝖣𝗈 𝗒𝗈𝗎 𝖶𝖺𝗇𝗍 𝖳𝗈 𝖨𝗇𝖽𝖾𝗑 𝖳𝗁𝗂𝗌 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 / 𝖦𝗋𝗈𝗎𝗉?\n\n𝖢𝗁𝖺𝗍 𝖨𝖣 / 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾: <code>{chat_id}</code>\n𝖫𝖺𝗌𝗍 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖨𝖣: <code>{last_msg_id}</code>',
            reply_markup=reply_markup)

    if type(chat_id) is int:
        try:
            link = (await bot.create_chat_invite_link(chat_id)).invite_link
        except ChatAdminRequired:
            return await message.reply('𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖨 a𝗆 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍 𝖺𝗇𝖽 𝗁𝖺𝗏𝖾 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝗂𝗇𝗏𝗂𝗍𝖾 𝗎𝗌𝖾𝗋𝗌.')
    else:
        link = f"@{message.forward_from_chat.username}"
    buttons = [
        [
            InlineKeyboardButton('𝗔𝗰𝗰𝗲𝗽𝘁 𝗜𝗻𝗱𝗲𝘅',
                                 callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('𝗥𝗲𝗷𝗲𝗰𝘁 𝗜𝗻𝗱𝗲𝘅',
                                 callback_data=f'index#reject#{chat_id}#{message.id}#{message.from_user.id}'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(LOG_CHANNEL,
                           f'#IndexRequest\n\n𝖡𝗒 : {message.from_user.mention} (<code>{message.from_user.id}</code>)\n𝖢𝗁𝖺𝗍 𝖨𝖣 / 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾 - <code> {chat_id}</code>\n𝖫𝖺𝗌𝗍 𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖨𝖣 - <code>{last_msg_id}</code>\n𝖨𝗇𝗏𝗂𝗍𝖾 𝖫𝗂𝗇𝗄 - {link}',
                           reply_markup=reply_markup)
    await message.reply('𝖳𝗁𝖺𝗇𝗄 𝖸𝗈𝗎 𝖿𝗈𝗋 𝗍𝗁𝖾 𝖢𝗈𝗇𝗍𝗋𝗂𝖻𝗎𝗍𝗂𝗈𝗇, 𝖶𝖺𝗂𝗍 𝖿𝗈𝗋 𝖬𝗒 𝖬𝗈𝖽𝖾𝗋𝖺𝗍𝗈𝗋𝗌 𝗍𝗈 𝗏𝖾𝗋𝗂𝖿𝗒 𝗍𝗁𝖾 𝖿𝗂𝗅𝖾𝗌.')


@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, message):
    if ' ' in message.text:
        _, skip = message.text.split(" ")
        try:
            skip = int(skip)
        except:
            return await message.reply("𝖲𝗄𝗂𝗉 𝗇𝗎𝗆𝖻𝖾𝗋 𝗌𝗁𝗈𝗎𝗅𝖽 𝖻𝖾 𝖺𝗇 𝗂𝗇𝗍𝖾𝗀𝖾𝗋.")
        await message.reply(f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗌𝖾𝗍 𝖲𝖪𝖨𝖯 𝗇𝗎𝗆𝖻𝖾𝗋 𝖺𝗌 {skip}")
        temp.CURRENT = int(skip)
    else:
        await message.reply("𝖦𝗂𝗏𝖾 𝗆𝖾 𝖺 𝗌𝗄𝗂𝗉 𝗇𝗎𝗆𝖻𝖾𝗋 𝖺𝗌 /setskip no. of messages to skip")


async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    async with lock:
        try:
            current = temp.CURRENT
            temp.CANCEL = False
            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                if temp.CANCEL:
                    await msg.edit(f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽!!\n\n𝖲𝖺𝗏𝖾𝖽 <code>{total_files}</code> 𝖿𝗂𝗅𝖾𝗌 𝗍𝗈 𝖽𝖺𝗍𝖺𝖡𝖺𝗌𝖾!\n𝖣𝗎𝗉𝗅𝗂𝖼𝖺𝗍𝖾 𝖥𝗂𝗅𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{duplicate}</code>\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{deleted}</code>\n𝖭𝗈𝗇-𝖬𝖾𝖽𝗂𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗌𝗄𝗂𝗉𝗉𝖾𝖽: <code>{no_media + unsupported}</code>(𝖴𝗇𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝖬𝖾𝖽𝗂𝖺 - `{unsupported}` )\n𝖤𝗋𝗋𝗈𝗋𝗌 𝖮𝖼𝖼𝗎𝗋𝗋𝖾𝖽: <code>{errors}</code>")
                    break
                current += 1
                if current % 20 == 0:
                    can = [[InlineKeyboardButton('𝗖𝗮𝗻𝗰𝗲𝗹', callback_data='index_cancel')]]
                    reply = InlineKeyboardMarkup(can)
                    await msg.edit_text(
                        text=f"𝖳𝗈𝗍𝖺𝗅 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝖿𝖾𝗍𝖼𝗁𝖾𝖽: <code>{current}</code>\n𝖳𝗈𝗍𝖺𝗅 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗌𝖺𝗏𝖾𝖽: <code>{total_files}</code>\n𝖣𝗎𝗉𝗅𝗂𝖼𝖺𝗍𝖾 𝖥𝗂𝗅𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{duplicate}</code>\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{deleted}</code>\n𝖭𝗈𝗇-𝖬𝖾𝖽𝗂𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗌𝗄𝗂𝗉𝗉𝖾𝖽: <code>{no_media + unsupported}</code>(𝖴𝗇𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝖬𝖾𝖽𝗂𝖺 - `{unsupported}` )\n𝖤𝗋𝗋𝗈𝗋𝗌 𝖮𝖼𝖼𝗎𝗋𝗋𝖾𝖽: <code>{errors}</code>",
                        reply_markup=reply)
                if message.empty:
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
                    unsupported += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    unsupported += 1
                    continue
                media.file_type = message.media.value
                media.caption = message.caption
                aynav, vnay = await save_file(media)
                if aynav:
                    total_files += 1
                elif vnay == 0:
                    duplicate += 1
                elif vnay == 2:
                    errors += 1
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'𝖤𝗋𝗋𝗈𝗋: {e}')
        else:
            await msg.edit(f'𝖲𝗎𝖼𝖼𝖾𝗌𝖿𝗎𝗅𝗅𝗒 𝗌𝖺𝗏𝖾𝖽 <code>{total_files}</code> 𝗍𝗈 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾!\n𝖣𝗎𝗉𝗅𝗂𝖼𝖺𝗍𝖾 𝖥𝗂𝗅𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{duplicate}</code>\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{deleted}</code>\n𝖭𝗈𝗇-𝖬𝖾𝖽𝗂𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗌𝗄𝗂𝗉𝗉𝖾𝖽: <code>{no_media + unsupported}</code>(𝖴𝗇𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝖬𝖾𝖽𝗂𝖺 - `{unsupported}` )\n𝖤𝗋𝗋𝗈𝗋𝗌 𝖮𝖼𝖼𝗎𝗋𝗋𝖾𝖽: <code>{errors}</code>')
