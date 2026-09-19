import os
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

app = Client(
    name="Nishimiya",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

async def get_target_user(client, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
            return user.id
        except:
            return None
    return None

# NO PREFIX NOW - prefixes=""
@app.on_message(filters.me & filters.command("ping", prefixes=""))
async def ping(client, message):
    await message.edit_text("Nishimiya is Alive! ⚡️")

@app.on_message(filters.me & filters.command("ban", prefixes=""))
async def ban_user(client, message: Message):
    user_id = await get_target_user(client, message)
    if not user_id:
        return await message.edit_text("Reply to a user or give username/id to ban.")
    try:
        await client.ban_chat_member(message.chat.id, user_id)
        await message.edit_text(f"Banned user {user_id}")
    except Exception as e:
        await message.edit_text(f"Failed: {e}")

@app.on_message(filters.me & filters.command("unban", prefixes=""))
async def unban_user(client, message: Message):
    user_id = await get_target_user(client, message)
    if not user_id:
        return await message.edit_text("Reply to a user to unban.")
    try:
        await client.unban_chat_member(message.chat.id, user_id)
        await message.edit_text(f"Unbanned user {user_id}")
    except Exception as e:
        await message.edit_text(f"Failed: {e}")

@app.on_message(filters.me & filters.command(["mute", "m"], prefixes=""))
async def mute_user(client, message: Message):
    user_id = await get_target_user(client, message)
    if not user_id:
        return await message.edit_text("Reply to user to mute.")
    try:
        await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
        await message.edit_text(f"Muted {user_id}")
    except Exception as e:
        await message.edit_text(f"Failed: {e}")

@app.on_message(filters.me & filters.command(["unmute", "um"], prefixes=""))
async def unmute_user(client, message: Message):
    user_id = await get_target_user(client, message)
    if not user_id:
        return await message.edit_text("Reply to user to unmute.")
    try:
        await client.restrict_chat_member(
            message.chat.id, user_id,
            ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
        )
        await message.edit_text(f"Unmuted {user_id}")
    except Exception as e:
        await message.edit_text(f"Failed: {e}")

@app.on_message(filters.me & filters.command("kick", prefixes=""))
async def kick_user(client, message: Message):
    user_id = await get_target_user(client, message)
    if not user_id:
        return await message.edit_text("Reply to user to kick.")
    try:
        await client.ban_chat_member(message.chat.id, user_id)
        await client.unban_chat_member(message.chat.id, user_id)
        await message.edit_text(f"Kicked {user_id}")
    except Exception as e:
        await message.edit_text(f"Failed: {e}")

@app.on_message(filters.me & filters.command("del", prefixes=""))
async def del_msg(client, message: Message):
    try:
        if message.reply_to_message:
            await message.reply_to_message.delete()
            await message.delete()
        else:
            await message.delete()
    except Exception as e:
        await message.edit_text(f"Failed: {e}")
@app.on_message(filters.me & filters.command("purge", prefixes=""))
async def purge(client, message: Message):
    if not message.reply_to_message:
        return await message.edit_text("Reply to a message to start purge from there.")
    start_id = message.reply_to_message.id
    end_id = message.id
    mids = [i for i in range(start_id, end_id)]
    try:
        await client.delete_messages(message.chat.id, mids)
    except Exception as e:
        await message.edit_text(f"Purge failed: {e}")

@app.on_message(filters.me & filters.command("pin", prefixes=""))
async def pin_msg(client, message: Message):
    if not message.reply_to_message:
        return await message.edit_text("Reply to message to pin.")
    try:
        await message.reply_to_message.pin()
        await message.edit_text("Pinned.")
    except Exception as e:
        await message.edit_text(f"Failed: {e}")

@app.on_message(filters.me & filters.command("unpin", prefixes=""))
async def unpin_msg(client, message: Message):
    if message.reply_to_message:
        try:
            await message.reply_to_message.unpin()
            await message.edit_text("Unpinned.")
        except Exception as e:
            await message.edit_text(f"Failed: {e}")
    else:
        try:
            await client.unpin_all_chat_messages(message.chat.id)
            await message.edit_text("Unpinned all.")
        except Exception as e:
            await message.edit_text(f"Failed: {e}")

print("Nishimiya Started!")
app.run()
