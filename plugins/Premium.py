# SPECIAL THANKS TO [Rishikesh Sharma] @Rk_botowner FOR THESE AMAZING CODES
# SPECIAL THANKS TO @DeletedFromEarth FOR MODIFYING THESE AMAZING CODES

from datetime import timedelta
import pytz
import datetime, time
from Script import script 
from info import ADMINS, PREMIUM_LOGS
from utils import get_seconds
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝗋𝖾𝗆𝗈𝗏𝖾𝖽 𝖿𝗋𝗈𝗆 𝗎𝗌𝖾𝗋 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>𝗛𝗲𝘆 {user.mention},\n\n𝗬𝗼𝘂𝗿 𝗽𝗿𝗲𝗺𝗶𝘂𝗺 𝗮𝗰𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗿𝗲𝗺𝗼𝘃𝗲𝗱.\n𝗧𝗵𝗮𝗻𝗸 𝘆𝗼𝘂 𝗳𝗼𝗿 𝘂𝘀𝗶𝗻𝗴 𝗼𝘂𝗿 𝘀𝗲𝗿𝘃𝗶𝗰𝗲. 😊\n𝗖𝗹𝗶𝗰𝗸 𝗼𝗻 /plan 𝘁𝗼 𝗰𝗵𝗲𝗰𝗸 𝗼𝘂𝘁 𝗼𝘁𝗵𝗲𝗿 𝗽𝗹𝗮𝗻𝘀.</b>"
            )
        else:
            await message.reply_text("𝖴𝗇𝖺𝖻𝗅𝖾 𝗍𝗈 𝗋𝖾𝗆𝗈𝗏𝖾 𝗎𝗌𝖾𝗋!\n𝖠𝗋𝖾 𝗒𝗈𝗎 𝗌𝗎𝗋𝖾, 𝗂𝗍 𝗐𝖺𝗌 𝖺 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗎𝗌𝖾𝗋 𝗂𝖽?")
    else:
        await message.reply_text("𝖴𝗌𝖺𝗀𝖾: /remove_premium user_id") 

@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    user = message.from_user.mention 
    user_id = message.from_user.id
    data = await db.get_user(message.from_user.id)  # Convert the user_id to integer
    if data and data.get("expiry_time"):
        #expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=data)
        expiry = data.get("expiry_time") 
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖳𝗂𝗆𝖾: %I:%M:%S %p")            
        # Calculate time difference
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
            
        # Calculate days, hours, and minutes
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
            
        # Format time left as a string
        time_left_str = f"{days} 𝖣𝖺𝗒𝗌, {hours} 𝖧𝗈𝗎𝗋𝗌, {minutes} 𝖬𝗂𝗇𝗎𝗍𝖾𝗌"
        await message.reply_text(f"⚜️ 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗨𝘀𝗲𝗿 𝗗𝗮𝘁𝗮:\n\n👤 𝖴𝗌𝖾𝗋: {user}\n⚡ 𝖴𝗌𝖾𝗋 𝖨𝖣: <code>{user_id}</code>\n⏰ 𝖳𝗂𝗆𝖾 𝖫𝖾𝖿𝗍: {time_left_str}\n⌛️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖣𝖺𝗍𝖾: {expiry_str_in_ist}")   
    else:
        await message.reply_text(f"𝖧𝖾𝗒 {user},\n\n𝖸𝗈𝗎 𝖽𝗈 𝗇𝗈𝗍 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝖺𝖼𝗍𝗂𝗏𝖾 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗉𝗅𝖺𝗇𝗌, 𝗂𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝗍𝖺𝗄𝖾 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗍𝗁𝖾𝗇 𝖼𝗅𝗂𝖼𝗄 𝗈𝗇 𝖻𝖾𝗅𝗈𝗐 𝖻𝗎𝗍𝗍𝗈𝗇 👇",
	reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 𝗖𝗵𝗲𝗰𝗸𝗼𝘂𝘁 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗣𝗹𝗮𝗻𝘀 💸", callback_data='seeplans')]]))			 

@Client.on_message(filters.command("get_premium") & filters.user(ADMINS))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await db.get_user(user_id)  # Convert the user_id to integer
        if data and data.get("expiry_time"):
            #expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=data)
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖳𝗂𝗆𝖾: %I:%M:%S %p")            
            # Calculate time difference
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            
            # Calculate days, hours, and minutes
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # Format time left as a string
            time_left_str = f"{days} 𝖣𝖺𝗒𝗌, {hours} 𝖧𝗈𝗎𝗋𝗌, {minutes} 𝖬𝗂𝗇𝗎𝗍𝖾𝗌"
            await message.reply_text(f"⚜️ 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗨𝘀𝗲𝗿 𝗗𝗮𝘁𝗮:\n\n👤 𝖴𝗌𝖾𝗋: {user.mention}\n⚡ 𝖴𝗌𝖾𝗋 𝖨𝖣: <code>{user_id}</code>\n⏰ 𝖳𝗂𝗆𝖾 𝖫𝖾𝖿𝗍: {time_left_str}\n⌛️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖣𝖺𝗍𝖾: {expiry_str_in_ist}")
        else:
            await message.reply_text("𝖭𝗈 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝖽𝖺𝗍𝖺 𝗈𝖿 𝗍𝗁𝖾 𝗎𝗌𝖾𝗋 𝗐𝖺𝗌 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾!")
    else:
        await message.reply_text("𝖴𝗌𝖺𝗀𝖾: /get_premium user_id")

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ 𝖩𝗈𝗂𝗇𝗂𝗇𝗀 𝖳𝗂𝗆𝖾: %I:%M:%S %p") 
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  # Using "id" instead of "user_id"  
            await db.update_user(user_data)  # Use the update_user method to update or insert user data
            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖳𝗂𝗆𝖾: %I:%M:%S %p")         
            await message.reply_text(f"𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖠𝖽𝖽𝖾𝖽 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 ✅\n\n👤 𝖴𝗌𝖾𝗋: {user.mention}\n⚡ 𝖴𝗌𝖾𝗋 𝖨𝖣: <code>{user_id}</code>\n⏰ 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖠𝖼𝖼𝖾𝗌𝗌: <code>{time}</code>\n\n⏳ 𝖩𝗈𝗂𝗇𝗂𝗇𝗀 𝖣𝖺𝗍𝖾: {current_time}\n\n⌛️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖣𝖺𝗍𝖾: {expiry_str_in_ist}", disable_web_page_preview=True)
            await client.send_message(
                chat_id=user_id,
                text=f"👋 𝖧𝖾𝗒 {user.mention},\n𝖳𝗁𝖺𝗇𝗄 𝗒𝗈𝗎 𝖿𝗈𝗋 𝗉𝗎𝗋𝖼𝗁𝖺𝗌𝗂𝗇𝗀 𝗉𝗋𝖾𝗆𝗂𝗎𝗆.\n𝖤𝗇𝗃𝗈𝗒!! ✨🎉\n\n⏰ 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖠𝖼𝖼𝖾𝗌𝗌: <code>{time}</code>\n⏳ 𝖩𝗈𝗂𝗇𝗂𝗇𝗀 𝖣𝖺𝗍𝖾: {current_time}\n\n⌛️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖣𝖺𝗍𝖾: {expiry_str_in_ist}", disable_web_page_preview=True              
            )    
            await client.send_message(PREMIUM_LOGS, text=f"#Added_Premium\n\n👤 𝖴𝗌𝖾𝗋: {user.mention}\n⚡ 𝖴𝗌𝖾𝗋 𝖨𝖣: <code>{user_id}</code>\n⏰ 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖠𝖼𝖼𝖾𝗌𝗌: <code>{time}</code>\n\n⏳ 𝖩𝗈𝗂𝗇𝗂𝗇𝗀 𝖣𝖺𝗍𝖾: {current_time}\n\n⌛️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖣𝖺𝗍𝖾: {expiry_str_in_ist}", disable_web_page_preview=True)
                    
        else:
            await message.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗍𝗂𝗆𝖾 𝖿𝗈𝗋𝗆𝖺𝗍. 𝖯𝗅𝖾𝖺𝗌𝖾 𝗎𝗌𝖾 '1 𝖽𝖺𝗒 𝖿𝗈𝗋 𝖽𝖺𝗒𝗌', '1 𝗁𝗈𝗎𝗋 𝖿𝗈𝗋 𝗁𝗈𝗎𝗋𝗌', 𝗈𝗋 '1 𝗆𝗂𝗇 𝖿𝗈𝗋 𝗆𝗂𝗇𝗎𝗍𝖾𝗌', 𝗈𝗋 '1 𝗆𝗈𝗇𝗍𝗁 𝖿𝗈𝗋 𝗆𝗈𝗇𝗍𝗁𝗌' 𝗈𝗋 '1 𝗒𝖾𝖺𝗋 𝖿𝗈𝗋 𝗒𝖾𝖺𝗋s'")
    else:
        await message.reply_text("𝖴𝗌𝖺𝗀𝖾: /add_premium user_id time (𝖾.𝗀., '1 𝖽𝖺𝗒 𝖿𝗈𝗋 𝖽𝖺𝗒𝗌', '1 𝗁𝗈𝗎𝗋 𝖿𝗈𝗋 𝗁𝗈𝗎𝗋𝗌', 𝗈𝗋 '1 𝗆𝗂𝗇 𝖿𝗈𝗋 𝗆𝗂𝗇𝗎𝗍𝖾𝗌', 𝗈𝗋 '1 𝗆𝗈𝗇𝗍𝗁 𝖿𝗈𝗋 𝗆𝗈𝗇𝗍𝗁𝗌' 𝗈𝗋 '1 𝗒𝖾𝖺𝗋 𝖿𝗈𝗋 𝗒𝖾𝖺𝗋s')")

@Client.on_message(filters.command("premium_users") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("<i>𝖥𝖾𝗍𝖼𝗁𝗂𝗇𝗀...</i>")
    new = f"⚜️ 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖴𝗌𝖾𝗋𝗌 𝖫𝗂𝗌𝗍:\n\n"
    user_count = 1
    users = await db.get_all_users()
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖳𝗂𝗆𝖾: %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"	 
            new += f"{user_count}. {(await client.get_users(user['id'])).mention}\n👤 𝖴𝗌𝖾𝗋 𝖨𝖣: {user['id']}\n⏳ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖣𝖺𝗍𝖾: {expiry_str_in_ist}\n⏰ 𝖳𝗂𝗆𝖾 𝖫𝖾𝖿𝗍: {time_left_str}\n"
            user_count += 1
        else:
            pass
    try:    
        await aa.edit_text(new)
    except MessageTooLong:
        with open('usersplan.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('usersplan.txt', caption="𝗣𝗮𝗶𝗱 𝗨𝘀𝗲𝗿𝘀:")



@Client.on_message(filters.command("plan"))
async def plan(client, message):
    user_id = message.from_user.id 
    users = message.from_user.mention 
    btn = [[
	
        InlineKeyboardButton("📲 𝗦𝗲𝗻𝗱 𝗣𝗮𝘆𝗺𝗲𝗻𝘁 𝗦𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁 𝗛𝗲𝗿𝗲", user_id=int(1101724431))],[InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", callback_data="close_data")
    ]]
    await message.reply_photo(photo="https://telegra.ph/file/4963dfeee700078956e76.jpg", caption=script.PREMIUM_TEXT.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
    
# SPECIAL THANKS TO [Rishikesh Sharma] @Rk_botowner FOR THESE AMAZING CODES
# SPECIAL THANKS TO @DeletedFromEarth FOR MODIFYING THESE AMAZING CODES 
