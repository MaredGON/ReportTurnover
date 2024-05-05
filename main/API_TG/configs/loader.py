from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from sys import exit

bot_token = "1870815171:AAGt85OXaCVXB3EhS1jfYocqLkQME2JpcfA"
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)