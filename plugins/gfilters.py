import io
from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.gfilters_mdb import(
   add_gfilter,
   get_gfilters,
   delete_gfilter,
   count_gfilters
)

from database.connections_mdb import active_connection
from utils import get_file_id, gfilterparser, split_quotes
from info import ADMINS


@Client.on_message(filters.command(['gfilter', 'addg']) & filters.incoming & filters.user(ADMINS))
async def addgfilter(client, message):
    args = message.text.html.split(None, 1)

    if len(args) < 2:
        await message.reply_text("𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖨𝗇𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾 :(", quote=True)
        return

    extracted = split_quotes(args[1])
    text = extracted[0].lower()

    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("𝖠𝖽𝖽 𝗌𝗈𝗆𝖾 𝖼𝗈𝗇𝗍𝖾𝗇𝗍 𝗍𝗈 𝗌𝖺𝗏𝖾 𝗒𝗈𝗎𝗋 𝖿𝗂𝗅𝗍𝖾𝗋!", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = gfilterparser(extracted[1], text)
        fileid = None
        if not reply_text:
            await message.reply_text("𝖸𝗈𝗎 𝖼𝖺𝗇𝗇𝗈𝗍 𝗁𝖺𝗏𝖾 𝖻𝗎𝗍𝗍𝗈𝗇𝗌 𝖺𝗅𝗈𝗇𝖾, 𝗀𝗂𝗏𝖾 𝗌𝗈𝗆𝖾 𝗍𝖾𝗑𝗍 𝗍𝗈 𝗀𝗈 𝗐𝗂𝗍𝗁 𝗂𝗍!", quote=True)
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = get_file_id(message.reply_to_message)
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None
            alert = None

    elif message.reply_to_message and message.reply_to_message.media:
        try:
            msg = get_file_id(message.reply_to_message)
            fileid = msg.file_id if msg else None
            reply_text, btn, alert = gfilterparser(extracted[1], text) if message.reply_to_message.sticker else gfilterparser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = gfilterparser(message.reply_to_message.text.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
    else:
        return

    await add_gfilter('gfilters', text, reply_text, btn, fileid, alert)

    await message.reply_text(
        f"GFilter for  `{text}`  added",
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )


@Client.on_message(filters.command(['viewgfilters', 'gfilters']) & filters.incoming & filters.user(ADMINS))
async def get_all_gfilters(client, message):
    texts = await get_gfilters('gfilters')
    count = await count_gfilters('gfilters')
    if count:
        gfilterlist = f"𝖳𝗈𝗍𝖺𝗅 𝗇𝗎𝗆𝖻𝖾𝗋 𝗈𝖿 𝗀𝖿𝗂𝗅𝗍𝖾𝗋𝗌 : {count}\n\n"

        for text in texts:
            keywords = " ×  `{}`\n".format(text)

            gfilterlist += keywords

        if len(gfilterlist) > 4096:
            with io.BytesIO(str.encode(gfilterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        gfilterlist = f"𝖳𝗁𝖾𝗋𝖾 𝖺𝗋𝖾 𝗇𝗈 𝖺𝖼𝗍𝗂𝗏𝖾 𝗀𝖿𝗂𝗅𝗍𝖾𝗋𝗌."

    await message.reply_text(
        text=gfilterlist,
        quote=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )
        
@Client.on_message(filters.command('delg') & filters.incoming & filters.user(ADMINS))
async def deletegfilter(client, message):
    try:
        cmd, text = message.text.split(" ", 1)
    except:
        await message.reply_text(
            "<i>𝖬𝖾𝗇𝗍𝗂𝗈𝗇 𝗍𝗁𝖾 𝗀𝖿𝗂𝗅𝗍𝖾𝗋 𝗇𝖺𝗆𝖾 𝗐𝗁𝗂𝖼𝗁 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾!</i>\n\n"
            "<code>/delg gfiltername</code>\n\n"
            "𝖴𝗌𝖾 /viewgfilters 𝗍𝗈 𝗏𝗂𝖾𝗐 𝖺𝗅𝗅 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗀𝖿𝗂𝗅𝗍𝖾𝗋𝗌",
            quote=True
        )
        return

    query = text.lower()

    await delete_gfilter(message, query, 'gfilters')

@Client.on_message(filters.command('delallg') & filters.user(ADMINS))
async def delallgfilters(client, message):
    await message.reply_text(
            f"𝖣𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖼𝗈𝗇𝗍𝗂𝗇𝗎𝖾??",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="𝗬𝗘𝗦",callback_data="gfiltersdeleteallconfirm")],
                [InlineKeyboardButton(text="𝗡𝗢",callback_data="gfiltersdeleteallcancel")]
            ]),
            quote=True
        )
