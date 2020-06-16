import config
import logic
import time
from . states import NettleBot
from aiogram import types
from misc import dp


@dp.callback_query_handler(lambda c: c.data == 'remember_mod1' or c.data == 'remember_mod2')
async def start_reminder_mod(call):
    param = ['быстро', 'качественно']
    await call.message.answer(f"Введите тему, которую хотите выучиить {param[int(call.data[-1]) - 1]}")
    reminder_mod_session = logic.BotMod(call.message, config.shelve_reminders_mods, int(call.data[-1]))
    reminder_mod_session.add_user_to_storage()
    await NettleBot.waiting_for_name_in_remembers_new_mod.set()


@dp.callback_query_handler(lambda c: c.data == 'remember_mod3')
async def show_all_reminders(call):
    reminder_date_session = logic.BotMod(call.message, config.shelve_reminders_dates)
    reminder_session = logic.BotMod(call.message, config.shelve_reminders)
    reminder_mod_session = logic.BotMod(call.message, config.shelve_reminders_mods)
    reminder_level_session = logic.BotMod(call.message, config.shelve_reminders_levels)
    mods = ['Быстрый', 'Долгий']
    list_of_dates = reminder_date_session.get_answer().split(' ')[:-1]
    list_of_reminders = reminder_session.get_answer().split(' ')[:-1]
    print(list_of_reminders)
    list_of_mods = reminder_mod_session.get_answer().split(' ')[:-1]
    list_of_levels = reminder_level_session.get_answer().split(' ')[:-1]
    await call.message.answer(f"У вас активировано {len(list_of_dates)} нап:")
    for i in range(len(list_of_dates)):
        #remained = (int(list_of_dates[i]) + logic.intervals_gen(int(list_of_mods[i]))[int(list_of_levels[i])] * 60 - int(time.time())) // 60
        await call.message.answer(f"Тема: {list_of_reminders[i].replace('!@$%^&*()_+', ' ')}\n"
                                  f"Режим: {mods[int(list_of_mods[i])]}\n")


@dp.message_handler(state=NettleBot.waiting_for_name_in_remembers_new_mod, content_types=types.ContentTypes.TEXT)
async def add_reminder(message, state):
    await state.finish()
    reminder_date_session = logic.BotMod(message, config.shelve_reminders_dates)
    reminder_level_session = logic.BotMod(message, config.shelve_reminders_levels)
    reminder_session = logic.BotMod(message, config.shelve_reminders)
    reminder_date_session.add_user_to_storage()
    reminder_session.add_user_to_storage()
    reminder_level_session.add_user_to_storage()
    await message.answer(f'Оповещение с темой "{message.text}" создано')
