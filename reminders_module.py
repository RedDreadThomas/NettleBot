import config
import shelve
import time
import logic
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from misc import bot


async def reminders_checker():
    reminders_dates = shelve.open(config.shelve_reminders_dates)
    reminders_levels = shelve.open(config.shelve_reminders_levels)
    reminders_reminders = shelve.open(config.shelve_reminders)
    reminders_mods = shelve.open(config.shelve_reminders_mods)
    for usr in reminders_dates:
        dates = reminders_dates[usr].split(' ')
        reminders = reminders_reminders[usr].split(' ')
        levels = reminders_levels[usr].split(' ')
        mods = reminders_mods[usr].split(' ')
        for date in dates:
            cur_date = int(date)
            cur_index = dates.index(date)
            cur_reminder = reminders[cur_index].replace('!@$%^&*()_+', ' ')
            cur_level = int(levels[cur_index])
            cur_mod = int(mods[cur_index])
            intervals = logic.intervals_gen(cur_mod)
            now_time = int(time.time())
            print(now_time - cur_date)
            if now_time - cur_date >= intervals[cur_level]:
                await bot.send_message(int(usr), f'Вам напоминание! Пришло время повторить изучаемый материал.\n'
                                                 f'{cur_reminder}')
                if cur_level == len(intervals) - 1:
                    await bot.send_message(int(usr), 'Поздравляем, теперь вы знаете материал намного лучше!\n'
                                                     'Уведомления по этой теме больше не будут приходить')
                    del dates[cur_index]
                    del levels[cur_index]
                    del reminders[cur_index]
                    del mods[cur_index]
                else:
                    dates[cur_index] = str(now_time)
                    levels[cur_index] = str(int(levels[cur_index]) + 1)
                    await bot.send_message(int(usr), f'Следующее напоминание придет через'
                                                     f' {intervals[int(levels[cur_index])] // 60} мин')
            if dates:
                reminders_dates[usr] = ' '.join(dates)
                reminders_levels[usr] = ' '.join(levels)
                reminders_reminders[usr] = ' '.join(reminders)
                reminders_mods[usr] = ' '.join(mods)
            else:
                del reminders_dates[usr]
                del reminders_levels[usr]
                del reminders_reminders[usr]
                del reminders_mods[usr]
            print(reminders_dates[usr], reminders_mods[usr], reminders_reminders[usr], reminders_levels[usr])

    reminders_dates.close()
    reminders_levels.close()
    reminders_reminders.close()
    reminders_mods.close()


scheduler = AsyncIOScheduler()
scheduler.add_job(reminders_checker, 'interval', seconds=60)
scheduler.start()

asyncio.get_event_loop().run_forever()
