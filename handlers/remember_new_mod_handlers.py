import config
import logic
import time
from handlers.choose_mod_handlers import remember_new
from aiogram.dispatcher import FSMContext
from handlers.states import NettleBot
from aiogram import types
from misc import dp
from emoji import emojize


@dp.callback_query_handler(lambda c: c.data == 'remember_mod1' or c.data == 'remember_mod2')
async def start_reminder_mod(call, state: FSMContext):
    param = ['как можно быстрее:', 'наиболее качественно:']
    keyboard = logic.Markup().pull([emojize(':left_arrow: Назад')], 'cancel_reminder_creation')
    await call.message.answer(f"Введите тему, которую хотите выучить {param[int(call.data[-1]) - 1]}",
                              reply_markup=keyboard)
    await state.update_data(mod=int(call.data[-1]) - 1)
    await NettleBot.waiting_for_name_in_remembers_new_mod.set()


@dp.callback_query_handler(lambda c: c.data == 'cancel_reminder_creation1')
async def clear_reminder_and_del_message(call):
    await call.message.delete()


@dp.callback_query_handler(lambda c: c.data == 'remember_mod3')
async def show_all_reminders(call):
    reminder_date_session = logic.BotMod(call.message, config.shelve_reminders_dates)
    reminder_session = logic.BotMod(call.message, config.shelve_reminders)
    reminder_mod_session = logic.BotMod(call.message, config.shelve_reminders_mods)
    reminder_level_session = logic.BotMod(call.message, config.shelve_reminders_levels)
    list_of_mods = ['Быстрый', 'Долгий']
    dates = reminder_date_session.get_answer()
    reminders = reminder_session.get_answer()
    mods = reminder_mod_session.get_answer()
    levels = reminder_level_session.get_answer()
    keyboard = logic.Markup().pull([emojize(':left_arrow: Назад')], 'return_from_all_reminders')

    if dates and reminders and levels and mods:
        dates = dates.split(' ')
        reminders = reminders.split(' ')
        mods = mods.split(' ')
        levels = levels.split(' ')
        print(levels, dates, mods, reminders)
        await call.message.answer(f"У вас активировано {len(dates)} нап:")
        for i in range(len(dates)):
            now_time = int(time.time())
            next_reminder_time = logic.intervals_gen(mods[i])[int(levels[i])] - (now_time - int(dates[i])) // 60
            await call.message.answer(f"{i + 1}.\n"
                                      f"Тема: {reminders[i].replace('!@$%^&*()_+', ' ')}\n"
                                      f"Режим: {list_of_mods[int(mods[i])]}\n"
                                      f"До следующего напоминания: {next_reminder_time} мин")
        await call.message.answer(f"Пока вы не можете удалять напоминания, но скоро мы обязательно добавим эту функцию."
                                  , reply_markup=keyboard)
    else:
        await call.message.answer("У вас не активровано ни одного напоминания.", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'return_from_all_reminders1' or c.data == 'return_from_create_reminder1')
async def return_to_start_reminder_mod(call):
    await remember_new(call)


@dp.message_handler(state=NettleBot.waiting_for_name_in_remembers_new_mod, content_types=types.ContentTypes.TEXT)
async def add_reminder(message, state: FSMContext):
    data = await state.get_data()
    mod = await data.get('mod')
    reminder_date_session = logic.BotMod(message, config.shelve_reminders_dates)
    reminder_level_session = logic.BotMod(message, config.shelve_reminders_levels)
    reminder_session = logic.BotMod(message, config.shelve_reminders)
    reminder_mod_session = logic.BotMod(message, config.shelve_reminders_mods, int(mod))
    reminder_date_session.add_user_to_storage()
    reminder_session.add_user_to_storage()
    reminder_level_session.add_user_to_storage()
    reminder_mod_session.add_user_to_storage()
    keyboard = logic.Markup().pull(['Готово'], 'return_from_create_reminder')
    await message.answer(f'Оповещение с темой "{message.text}" создано', reply_markup=keyboard)
