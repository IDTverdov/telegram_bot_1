import logging
import vk_api
import config as cfg
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, executor, types
from get_vk import get_wall_posts, cut_file


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')
vk_session = vk_api.VkApi(token=cfg.TOKEN_VK)
vk_session.get_api()
bot = Bot(cfg.TOKEN_TELEGRAM)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"], commands_prefix='/')
async def start(message: types.Message):
    if message.chat.id == int(cfg.CHAT_ID):
        await message.answer('Привет! Я пришлю запись со стены ВК')
    else:
        await message.answer('Добрый день! Этот бот доступен только админам сообщества ROLLIN RPG KZN')


@dp.message_handler(commands=["test"], commands_prefix='/')
async def start(message: types.Message):
    await message.answer(f'Работаю-с!, chat_id={message.chat.id}')


async def send_post(bot):
    send_list = get_wall_posts()
    if len(send_list) == 1:
        await bot.send_message(cfg.CHAT_ID, send_list[0])
    else:
        await bot.send_photo(cfg.CHAT_ID, photo=send_list[1], caption=send_list[0])

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(send_post, trigger='interval', seconds=10, kwargs={'bot': bot})
scheduler.add_job(cut_file, trigger='interval', days=1)


if __name__ == '__main__':
    scheduler.start()
    logging.info('Bot started!')
    executor.start_polling(dp, skip_updates=True)

