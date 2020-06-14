import config
import logic
import time
from misc import dp, bot


@dp.callback_query_handler(lambda c: c.data == 'remember_mod1' or c.data == 'remember_mod2')
async def add_reminder(call):
    reminder_session = logic.MindGame(bot, call.message, config.shelve_date)
    reminder_level_session = logic.MindGame(bot, call.message, config.shelve_lvl_of_reminders)
    if reminder_session.user_in_players():
        informer_message = await call.message.answer("У вас уже созданы напоминания, если хотите создать новые, "
                                                     "сначала удалите старые!")
        time.sleep(3)
        await informer_message.delete()
    else:
        reminder_session.add_user_to_players()
        reminder_level_session.add_user_to_players()
