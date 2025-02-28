from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from info import ADMINS
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"𝖸𝗈𝗎 𝖺𝗋𝖾 𝖺𝗇𝗈𝗇𝗒𝗆𝗈𝗎𝗌 𝖺𝖽𝗆𝗂𝗇. 𝖴𝗌𝖾 /connect {message.chat.id} 𝗂𝗇 𝖯𝖬")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        try:
            cmd, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(
                "<b>𝖤𝗇𝗍𝖾𝗋 𝗂𝗇 𝖼𝗈𝗋𝗋𝖾𝖼𝗍 𝖿𝗈𝗋𝗆𝖺𝗍!</b>\n\n"
                "<code>/connect groupid</code>\n\n"
                "<i>𝖦𝖾𝗍 𝗒𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 𝗂𝖽 𝖻𝗒 𝖺𝖽𝖽𝗂𝗇𝗀 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍 𝗍𝗈 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝖺𝗇𝖽 𝗎𝗌𝖾  <code>/id</code></i>",
                quote=True
            )
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and userid not in ADMINS
        ):
            await message.reply_text("𝖸𝗈𝗎 𝗌𝗁𝗈𝗎𝗅𝖽 𝖻𝖾 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗀𝗂𝗏𝖾𝗇 𝗀𝗋𝗈𝗎𝗉!", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖦𝗋𝗈𝗎𝗉 𝖨𝖣!\n\n𝖨𝖿 𝖼𝗈𝗋𝗋𝖾𝖼𝗍, 𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖨'𝗆 𝗉𝗋𝖾𝗌𝖾𝗇𝗍 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉!!",
            quote=True,
        )

        return
    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == enums.ChatMemberStatus.ADMINISTRATOR:
            ttl = await client.get_chat(group_id)
            title = ttl.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await message.reply_text(
                    f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗍𝗈 **{title}**\n𝖭𝗈𝗐 𝗆𝖺𝗇𝖺𝗀𝖾 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝖿𝗋𝗈𝗆 𝗆𝗒 𝗉𝗆!",
                    quote=True,
                    parse_mode=enums.ParseMode.MARKDOWN
                )
                if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    await client.send_message(
                        userid,
                        f"Connected to **{title}** !",
                        parse_mode=enums.ParseMode.MARKDOWN
                    )
            else:
                await message.reply_text(
                    "𝖸𝗈𝗎'𝗋𝖾 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗍𝗈 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍!",
                    quote=True
                )
        else:
            await message.reply_text("𝖠𝖽𝖽 𝗆𝖾 𝖺𝗌 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉", quote=True)
    except Exception as e:
        logger.exception(e)
        await message.reply_text('𝖲𝗈𝗆𝖾 𝖾𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽! 𝖳𝗋𝗒 𝖺𝗀𝖺𝗂𝗇 𝗅𝖺𝗍𝖾𝗋.', quote=True)
        return


@Client.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def deleteconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"𝖸𝗈𝗎 𝖺𝗋𝖾 𝖺𝗇𝗈𝗇𝗒𝗆𝗈𝗎𝗌 𝖺𝖽𝗆𝗂𝗇. 𝖴𝗌𝖾 /connect {message.chat.id} 𝗂𝗇 𝖯𝖬")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text("𝖱𝗎𝗇 /connections 𝗍𝗈 𝗏𝗂𝖾𝗐 𝗈𝗋 𝖽𝗂𝗌𝖼𝗈𝗇𝗇𝖾𝖼𝗍 𝖿𝗋𝗈𝗆 𝗀𝗋𝗈𝗎𝗉𝗌!", quote=True)

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            return

        delcon = await delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text("𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝗂𝗌𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝖿𝗋𝗈𝗆 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍", quote=True)
        else:
            await message.reply_text("𝖳𝗁𝗂𝗌 𝖼𝗁𝖺𝗍 𝗂𝗌𝗇'𝗍 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗍𝗈 𝗆𝖾!\n𝖣𝗈 /connect 𝗍𝗈 𝖼𝗈𝗇𝗇𝖾𝖼𝗍.", quote=True)


@Client.on_message(filters.private & filters.command(["connections"]))
async def connections(client, message):
    userid = message.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        await message.reply_text(
            "𝖳𝗁𝖾𝗋𝖾 𝖺𝗋𝖾 𝗇𝗈 𝖺𝖼𝗍𝗂𝗏𝖾 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝗂𝗈𝗇𝗌!! 𝖢𝗈𝗇𝗇𝖾𝖼𝗍 𝗍𝗈 𝗌𝗈𝗆𝖾 𝗀𝗋𝗈𝗎𝗉𝗌 𝖿𝗂𝗋𝗌𝗍.",
            quote=True
        )
        return
    buttons = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " - ACTIVE" if active else ""
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                    )
                ]
            )
        except:
            pass
    if buttons:
        await message.reply_text(
            "𝖸𝗈𝗎𝗋 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗀𝗋𝗈𝗎𝗉 𝖽𝖾𝗍𝖺𝗂𝗅𝗌:\n\n",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.reply_text(
            "𝖳𝗁𝖾𝗋𝖾 𝖺𝗋𝖾 𝗇𝗈 𝖺𝖼𝗍𝗂𝗏𝖾 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝗂𝗈𝗇𝗌!! 𝖢𝗈𝗇𝗇𝖾𝖼𝗍 𝗍𝗈 𝗌𝗈𝗆𝖾 𝗀𝗋𝗈𝗎𝗉𝗌 𝖿𝗂𝗋𝗌𝗍.",
            quote=True
        )
