import os
import time
from datetime import datetime
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

# GLOBALS
is_afk = False
afk_reason = None
afk_start = None
original_profile = None
original_photo = None

async def get_target_user(client, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
            return user
        except:
            return None
    return None

@app.on_message(filters.me & filters.command("ping", prefixes=""))
async def ping(client, message):
    start = time.time()
    m = await message.edit_text("⚡️ Pinging...")
    end = time.time()
    latency = round((end - start) * 1000)
    await m.edit_text(f"Nishimiya is Alive! ✨\nLatency: {latency}ms 🚀")

@app.on_message(filters.me & filters.command("ban", prefixes=""))
async def ban_user(client, message: Message):
    user = await get_target_user(client, message)
    if not user:
        return await message.edit_text("❌ Reply to a user to ban.")
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await message.edit_text(f"🔨 Banned {user.first_name} ✅")
    except Exception as e:
        await message.edit_text(f"❌ Failed: {e}")

@app.on_message(filters.me & filters.command("unban", prefixes=""))
async def unban_user(client, message: Message):
    user = await get_target_user(client, message)
    if not user:
        return await message.edit_text("❌ Reply to a user to unban.")
    try:
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit_text(f"♻️ Unbanned {user.first_name} ✅")
    except Exception as e:
        await message.edit_text(f"❌ Failed: {e}")

@app.on_message(filters.me & filters.command("mute", prefixes=""))
async def mute_user(client, message: Message):
    user = await get_target_user(client, message)
    if not user:
        return await message.edit_text("❌ Reply to user to mute.")
    try:
        await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions())
        await message.edit_text(f"🔇 Muted {user.first_name} 🤫")
    except Exception as e:
        await message.edit_text(f"❌ Failed: {e}")

@app.on_message(filters.me & filters.command("unmute", prefixes=""))
async def unmute_user(client, message: Message):
    user = await get_target_user(client, message)
    if not user:
        return await message.edit_text("❌ Reply to user to unmute.")
    try:
        await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_send_polls=True))
        await message.edit_text(f"🔊 Unmuted {user.first_name} ✅")
    except Exception as e:
        await message.edit_text(f"❌ Failed: {e}")

@app.on_message(filters.me & filters.command("kick", prefixes=""))
async def kick_user(client, message: Message):
    user = await get_target_user(client, message)
    if not user:
        return await message.edit_text("❌ Reply to user to kick.")
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit_text(f"👢 Kicked {user.first_name} 💨")
    except Exception as e:
        await message.edit_text(f"❌ Failed: {e}")

@app.on_message(filters.me & filters.command("promote", prefixes=""))
async def promote_user(client, message: Message):
    user = await get_target_user(client, message)
    if not user:
        return await message.edit_text("❌ Reply to user to promote.")
    try:
        await client.promote_chat_member(message.chat.id, user.id, can_manage_chat=True, can_delete_messages=True, can_manage_video_chats=True, can_restrict_members=True, can_change_info=True, can_invite_users=True, can_pin_messages=True)
        await message.edit_text(f"⬆️ Promoted {user.first_name} to admin 👑")
    except Exception as e:
        await message.edit_text(f"❌ Failed: {e}")

@app.on_message(filters.me & filters.command("demote", prefixes=""))
async def demote_user(client, message: Message):
    user = await get_target_user(client, message)
    if not user:
        return await message.edit_text("❌ Reply to user to demote.")
    try:
        await client.promote_chat_member(message.chat.id, user.id, can_manage_chat=False, can_delete_messages=False, can_manage_video_chats=False, can_restrict_members=False, can_change_info=False, can_invite_users=False, can_pin_messages=False)
        await message.edit_text(f"⬇️ Demoted {user.first_name} 😶‍🌫️")
    except Exception as e:
        await message.edit_text(f"❌ Failed: {e}")

@app.on_message(filters.me & filters.command(["del", "delete"], prefixes=""))
async def del_msg(client, message: Message):
    try:
        if message.reply_to_message:
            await message.reply_to_message.delete()
            await message.delete()
        else:
            await message.delete()
    except Exception as e:
        await message.edit_text(f"❌ Error: {e}")

@app.on_message(filters.me & filters.command("purge", prefixes=""))
async def purge(client, message: Message):
    if not message.reply_to_message:
        return await message.edit_text("❌ Reply to a message to start purge 🧹")
    start_id = message.reply_to_message.id
    end_id = message.id
    mids = [i for i in range(start_id, end_id)]
    try:
        await client.delete_messages(message.chat.id, mids)
    except Exception as e:
        await message.edit_text(f"❌ Error: {e}")

@app.on_message(filters.me & filters.command("pin", prefixes=""))
async def pin_msg(client, message: Message):
    if not message.reply_to_message:
        return await message.edit_text("❌ Reply to message to pin 📌")
    try:
        await message.reply_to_message.pin()
        await message.edit_text("📌 Pinned! ✅")
    except Exception as e:
        await message.edit_text(f"❌ Error: {e}")

@app.on_message(filters.me & filters.command("unpin", prefixes=""))
async def unpin_msg(client, message: Message):
    try:
        if message.reply_to_message:
            await message.reply_to_message.unpin()
            await message.edit_text("📍 Unpinned! ✅")
        else:
            await client.unpin_all_chat_messages(message.chat.id)
            await message.edit_text("📍 Unpinned all! ✅")
    except Exception as e:
        await message.edit_text(f"❌ Error: {e}")

# --- EDITED: NOW WITH DOT PREFIX ---
@app.on_message(filters.me & filters.command("clone", prefixes="."))
async def clone_user(client, message: Message):
    global original_profile, original_photo
    user = await get_target_user(client, message)
    if not user:
        return await message.edit_text("❌ Reply to a user to clone his profile 👤\nUse: .clone reply to user")

    await message.edit_text(f"🎭 Cloning {user.first_name}...")

    try:
        me = await client.get_me()
        my_full = await client.get_chat(me.id)
        original_profile = {
            "first_name": me.first_name,
            "last_name": me.last_name or "",
            "bio": my_full.bio or ""
        }
        try:
            async for photo in client.get_chat_photos("me", limit=1):
                original_photo = photo.file_id
        except:
            pass

        target_chat = await client.get_chat(user.id)
        target_bio = target_chat.bio or ""
        pfp_file = None
        async for photo in client.get_chat_photos(user.id, limit=1):
            pfp_file = await client.download_media(photo.file_id)

        await client.update_profile(first_name=user.first_name or " ", last_name=user.last_name or "", bio=target_bio)
        if pfp_file:
            await client.set_profile_photo(photo=pfp_file)
            os.remove(pfp_file)

        await message.edit_text(f"✅ Successfully cloned {user.first_name} 🎭✨")
    except Exception as e:
        await message.edit_text(f"❌ Clone failed: {e}")

# --- EDITED: NOW.rev WITH DOT PREFIX ---
@app.on_message(filters.me & filters.command(["rev", "reverse", "unclone"], prefixes="."))
async def reverse_clone(client, message: Message):
    global original_profile
    if not original_profile:
        return await message.edit_text("❌ No cloned profile found to reverse. 😕")

    await message.edit_text("🔄 Reversing clone...")
    try:
        await client.update_profile(first_name=original_profile["first_name"], last_name=original_profile["last_name"], bio=original_profile["bio"])
        try:
            async for photo in client.get_chat_photos("me", limit=1):
                await client.delete_profile_photos(photo.file_id)
        except:
            pass

        await message.edit_text("✅ Reversed to original profile! 🙏✨")
        original_profile = None
    except Exception as e:
        await message.edit_text(f"❌ Reverse failed: {e}")

@app.on_message(filters.me & filters.command("gc", prefixes=""))
async def create_gc(client, message: Message):
    if len(message.command) < 3:
        return await message.edit_text("❌ Format: gc MyGroup @username 📝")

    gc_name = message.command[1]
    target_username = message.command[2]

    if len(message.command) > 3:
        gc_name = " ".join(message.command[1:-1])
        target_username = message.command[-1]

    try:
        user_to_add = await client.get_users(target_username)
    except Exception as e:
        return await message.edit_text(f"❌ Can't find user {target_username}: {e}")

    await message.edit_text(f"👥 Creating group {gc_name} with {user_to_add.first_name}...")
    try:
        group = await client.create_group(title=gc_name, users=[user_to_add.id])
        await message.edit_text(f"✅ Group {gc_name} created! 🎉\nID: {group.id}")
    except Exception as e:
        await message.edit_text(f"❌ GC failed: {e}")

@app.on_message(filters.me & filters.command("info", prefixes=""))
async def info_user(client, message: Message):
    user = await get_target_user(client, message)
    if not user:
        user = await client.get_me()
        target_chat = await client.get_chat(user.id)
    else:
        try:
            target_chat = await client.get_chat(user.id)
        except:
            target_chat = None

    bio = target_chat.bio if target_chat and target_chat.bio else "No bio"
    username = f"@{user.username}" if user.username else "No username"

    caption = f"""
👤 User Info ✨

Name: {user.first_name} {user.last_name or ''}
Username: {username} 🔗
ID: {user.id} 🆔
Bio: {bio} 📝
Is Bot: {user.is_bot} 🤖
Is Premium: {user.is_premium or False} ⭐
"""
    try:
        async for photo in client.get_chat_photos(user.id, limit=1):
            await client.send_photo(message.chat.id, photo.file_id, caption=caption)
            await message.delete()
            return
    except:
        pass

    await message.edit_text(caption)

@app.on_message(filters.me & filters.command("afk", prefixes=""))
async def set_afk(client, message: Message):
    global is_afk, afk_reason, afk_start
    is_afk = True
    afk_reason = " ".join(message.command[1:]) if len(message.command) > 1 else None
    afk_start = datetime.now()
    text = "😴 AFK Mode Enabled!"
    if afk_reason:
        text += f"\nReason: {afk_reason} 💭"
    await message.edit_text(text)
    @app.on_message(filters.me, group=2)
async def back_from_afk(client, message: Message):
    global is_afk, afk_reason, afk_start
    if is_afk and not message.text.lower().startswith("afk"):
        is_afk = False
        duration = datetime.now() - afk_start if afk_start else None
        time_msg = ""
        if duration:
            mins = int(duration.total_seconds() // 60)
            if mins > 0:
                time_msg = f" ({mins}m away)"
        await message.reply_text(f"👋 I'm back online! ✨{time_msg}")
        afk_reason = None
        afk_start = None

@app.on_message((filters.mentioned | filters.private) & ~filters.me & ~filters.bot, group=3)
async def afk_reply(client, message: Message):
    global is_afk, afk_reason
    if is_afk:
        reply_text = "😴 The Person is Currently Offline 😴"
        if afk_reason:
            reply_text += f"\n\nReason: {afk_reason} 💭"
        try:
            await message.reply_text(reply_text)
        except:
            pass

print("Nishimiya Started!")
app.run()
