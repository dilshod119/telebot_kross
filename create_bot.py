from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

bot = Bot(token='5584546585:AAFBL-BCBG9Kn9zn-ZN989Th4jhomXUFWxc')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)