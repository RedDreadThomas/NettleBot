from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import config
import shelve
import time
import asyncio
from misc import bot


async def reminders_checker():
    intervals = [1, 2, 3]
    now_time = time.time()
    reminders = shelve.open(config.shelve_date)
    reminders_level = shelve.open(config.shelve_lvl_of_reminders)
    for usr in reminders:
        if (now_time - reminders[usr]) // 60 >= intervals[reminders_level[usr]]:
            await bot.send_message(int(usr), "Напоминание: вам нужно повторить тему!")
            reminders[usr] = now_time
            reminders_level[usr] += 1
    reminders.close()
    reminders_level.close()

scheduler = AsyncIOScheduler()
scheduler.add_job(reminders_checker, 'interval', seconds=60)
scheduler.start()

asyncio.get_event_loop().run_forever()
