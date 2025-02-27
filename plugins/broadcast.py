from pyrogram import Client, filters
import datetime
import time
from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages, broadcast_messages_group
import asyncio
        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
# https://t.me/GetTGLink/4178
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀 𝗒𝗈𝗎𝗋 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌...'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝗂𝗇 𝗉𝗋𝗈𝗀𝗋𝖾𝗌𝗌:\n\n𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌: {total_users}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_users}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}\n𝖡𝗅𝗈𝖼𝗄𝖾𝖽: {blocked}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽:\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝗂𝗇 {time_taken} 𝗌𝖾𝖼𝗈𝗇𝖽𝗌.\n\n𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌: {total_users}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_users}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}\n𝖡𝗅𝗈𝖼𝗄𝖾𝖽: {blocked}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}")

@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_group(bot, message):
    groups = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀 𝗒𝗈𝗎𝗋 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗍𝗈 𝗀𝗋𝗈𝗎𝗉𝗌...'
    )
    start_time = time.time()
    total_groups = await db.total_chat_count()
    done = 0
    failed =0

    success = 0
    async for group in groups:
        pti, sh = await broadcast_messages_group(int(group['id']), b_msg)
        if pti:
            success += 1
        elif sh == "Error":
                failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝗂𝗇 𝗉𝗋𝗈𝗀𝗋𝖾𝗌𝗌:\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌 {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽:\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝗂𝗇 {time_taken} 𝗌𝖾𝖼𝗈𝗇𝖽𝗌.\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌 {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}")
        
