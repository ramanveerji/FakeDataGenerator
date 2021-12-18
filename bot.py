import asyncio
import requests
import os
import logging
import time
import string
import random
import html

# for fake dats.
from faker import Faker
from faker.providers import internet

# telethon
from telethon import events, Button, TelegramClient
from telethon.tl import functions, types
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

logging.basicConfig(level=logging.INFO)

try:
    API_ID = int(os.environ.get("API_ID", 6))
    API_HASH = os.environ.get("API_HASH", None)
    TOKEN = os.environ.get("TOKEN", None)
except ValueError:
    print("You forgot to fullfill vars")
    print("Bot is quitting....")
    exit()
except Exception as e:
    print(f'Error - {e}')
    print("Bot is quitting.....")
    exit()
except ApiIdInvalidError:
    print("Your API_ID or API_HASH is Invalid.")
    print("Bot is quitting.")
    exit()

bot = TelegramClient('oxi', API_ID, API_HASH)
oxi = bot.start(bot_token=TOKEN)


# fake data generator
async def is_admin(event, user):
    try:
        sed = await event.client.get_permissions(event.chat_id, user)
        is_mod = bool(sed.is_admin)
    except:
        is_mod = False
    return is_mod

@oxi.on(events.NewMessage(pattern="^[!?/]gen"))
async def hi(event):
    if event.fwd_from:
        return
    if event.is_group and not await is_admin(event, event.message.sender_id):
        await event.reply("`You Should Be Admin To Do This!`")
        return
    fake = Faker()
    print("FAKE DETAILS GENERATED\n")
    name = str(fake.name())
    fake.add_provider(internet)
    address = str(fake.address())
    ip = fake.ipv4_private()
    cc = fake.credit_card_full()
    email = fake.ascii_free_email()
    job = fake.job()
    android = fake.android_platform_token()
    pc = fake.chrome()
    await event.reply(
        f"<b><u> Fake Information Generated</b></u>\n<b>Name :-</b><code>{name}</code>\n\n<b>Address:-</b><code>{address}</code>\n\n<b>IP ADDRESS:-</b><code>{ip}</code>\n\n<b>credit card:-</b><code>{cc}</code>\n\n<b>Email Id:-</b><code>{email}</code>\n\n<b>Job:-</b><code>{job}</code>\n\n<b>android user agent:-</b><code>{android}</code>\n\n<b>Pc user agent:-</b><code>{pc}</code>",
        parse_mode="HTML",
    )

# start handler

@oxi.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    if event.is_group:
        await event.reply("**Bot is alive**")
        return
    await event.reply(f"**Hello👋 {event.sender.first_name}**\nI'm a Fake Data generator bot. I can generate fake Data's  randomly.",
                    buttons=[
                        [Button.url("source code", url="https://github.com/Oxidisedman/FakeDataGenerator")],
                        [Button.inline("Help",data="help")]
                    ])

@oxi.on(events.callbackquery.CallbackQuery(data="help"))
async def ex(event):
    await event.edit("**Actually, it's not a complecated task.**\n `/gen`: **For generate fake Data.**")

print ("Successfully Started")
oxi.run_until_disconnected()
