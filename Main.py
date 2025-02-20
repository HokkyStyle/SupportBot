import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest, TelegramConflictError
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = ''
CHANNELS_FILE = "channels.json"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
MESSAGE_TEXT = "Пост для редактирования."

try:
    with open(CHANNELS_FILE, 'r') as f:
        channel_ids = set(json.load(f))
except FileNotFoundError:
    channel_ids = set()


@dp.channel_post()
async def channel_post(message: Message):
    channel_id = message.chat.id
    if channel_id not in channel_ids:
        channel_ids.add(channel_id)
        with open(CHANNELS_FILE, 'w') as f:
            json.dump(list(channel_ids), f)
        print(f"Бот был добавлен в канал с ID: {channel_id}")


async def send_message(channel_id, text):
    try:
        await bot.send_message(channel_id, text)
    except TelegramForbiddenError:
        logging.error(f"Bot is not a member of the channel {channel_id}")
    except TelegramBadRequest as e:
        logging.error(f"Failed to send message to channel {channel_id}: {e}")


async def send_photo(channel_id, photo, caption):
    try:
        await bot.send_photo(channel_id, photo=photo, caption=caption)
    except TelegramForbiddenError:
        logging.error(f"Bot is not a member of the channel {channel_id}")
    except TelegramBadRequest as e:
        logging.error(f"Failed to send photo to channel {channel_id}: {e}")


methods = [(send_message, (MESSAGE_TEXT,)), (send_photo, ('https://postimg.cc/gxV8Rf34', MESSAGE_TEXT))]
currents_method_index = 0


async def send_to_channels():
    global currents_method_index
    while True:
        for channel_id in channel_ids:
            method, args = methods[currents_method_index]  
            await method(channel_id, *args)  
            currents_method_index = (currents_method_index + 1) % len(methods)  
            await asyncio.sleep(0.05)
        await asyncio.sleep(60 * 60 * 6)


async def main():
    try:
        send_task = asyncio.create_task(send_to_channels())
        polling_task = asyncio.create_task(dp.start_polling(bot))
        await asyncio.gather(send_task, polling_task)
    except TelegramConflictError:
        logging.error(
            "Conflict: terminated by other getUpdates request; make sure that only one bot instance is running")


if __name__ == '__main__':
    asyncio.run(main())
