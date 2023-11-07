from brain import chatbot
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums
from config import *

ana = Client(
    name="ana",
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
    bot_token=TELEGRAM_BOT_TOKEN,
)


@ana.on_message(filters.command("start"))
async def start_cmd(client: ana, msg: Message):
    await client.send_message(
        chat_id=msg.chat.id,
        text=f"Hey!! `{msg.from_user.first_name}`, I'm a simple chatbot based on openai api. I can understand your problems and reply with the desired solutions.\n\nI'm devloped by [Minkxx](https://t.me/minkxx69). Thanks for using me.",
        reply_to_message_id=msg.id,
        disable_web_page_preview=True,
    )
    

cb = chatbot(OPENAI_API_KEY, "roles//default_chat.json")

@ana.on_message(filters.command("clear"))
async def clear_chat(client: ana, msg: Message):
    cb.clear()
    await client.send_message(
        chat_id=msg.chat.id,
        text="Chat cleared!!",
        reply_to_message_id=msg.id,
        disable_web_page_preview=True,
    )
    # pass


@ana.on_message(filters.incoming)
async def incoming_messages(client: ana, msg: Message):
    await client.send_chat_action(msg.chat.id, enums.ChatAction.TYPING)
    ai_msg = cb.chat(msg.text)
    await client.send_message(
        chat_id=msg.chat.id,
        text=ai_msg,
        reply_to_message_id=msg.id,
        disable_web_page_preview=True,
    )

print("bot started")
ana.run()