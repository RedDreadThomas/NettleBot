import logging
from aiogram import Bot, Dispatcher
import config

bot = Bot(token=config.token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
