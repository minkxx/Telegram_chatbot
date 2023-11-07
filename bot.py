import os
from brain import chatbot, newChat
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

cb = chatbot(OPENAI_API_KEY)


@ana.on_message(filters.command("start"))
async def start_cmd(client: ana, msg: Message):
    await client.send_message(
        chat_id=msg.chat.id,
        text=f"Hey!! `{msg.from_user.first_name}`, I'm a simple chatbot based on openai api. I can understand your problems and reply with the desired solutions.\n\nI'm devloped by [Minkxx](https://t.me/minkxx69). Thanks for using me.",
        reply_to_message_id=msg.id,
        disable_web_page_preview=True,
    )


@ana.on_message(filters.command("new_chat"))
async def new_chat(client: ana, msg: Message):
    chat_path = f"roles//{msg.from_user.id}_chat.json"
    if os.path.exists(chat_path):
        await client.send_message(
            chat_id=msg.chat.id,
            text="Chat already exists",
            reply_to_message_id=msg.id,
        )
    else:
        newChat(chat_path)
        await client.send_message(
            chat_id=msg.chat.id,
            text=f"Chat created!\n{chat_path}",
            reply_to_message_id=msg.id,
        )


@ana.on_message(filters.command("clear"))
async def clear_chat(client: ana, msg: Message):
    cb.clear()
    await client.send_message(
        chat_id=msg.chat.id,
        text="Chat cleared!!",
        reply_to_message_id=msg.id,
    )
#TODO: fix chat clear

@ana.on_message(filters.command("get_chat"))
async def get_chat(client: ana, msg: Message):
    chat_path = f"roles//{msg.from_user.id}_chat.json"
    if os.path.exists(chat_path):
        await client.send_document(
            chat_id=msg.chat.id,
            document=chat_path,
            caption="Here is you chat history in json format.",
            reply_to_message_id=msg.id,

        )
    else:
        await client.send_message(
            chat_id=msg.chat.id,
            text="No chat found!",
            reply_to_message_id=msg.id,
        )

@ana.on_message(filters.incoming)
async def incoming_messages(client: ana, msg: Message):
    chat_path = f"roles//{msg.from_user.id}_chat.json"
    if os.path.exists(chat_path):
        ai_msg = cb.chat(msg.text, chat_path)
        await client.send_message(
            chat_id=msg.chat.id,
            text=ai_msg,
            reply_to_message_id=msg.id,
        )
    else:
        await client.send_message(
            chat_id=msg.chat.id,
            text="To interact with me you first need to create a chat first\n/new_chat",
            reply_to_message_id=msg.id,
        )

print("bot started")
ana.run()