import time
from aiogram import types
from aiogram.utils import executor
from emoji import emojize

import logic
import config
import handlers
from misc import dp, bot


@dp.message_handler(lambda message: True, content_types=["text"])
async def text_checker(message):
    """
    Эта функция обрабатывает все текстовые сообщения и
    1) Удаляет спам
    2) Завершает игру(проверяет правильность ответа, обновляет уровень пользователя)
    :param message: (types.Message)
    :return:
    """
    chat_id = message.chat.id
    whats_game = logic.MindGame(bot, message, 'search', 0).generate()
    if not whats_game:
        await bot.delete_message(chat_id, message.message_id)
    elif whats_game == config.numbers_answers:
        game = logic.MindGame(bot, message, config.numbers_answers, logic.get_difficulty(chat_id))
        answer = ''.join(game.get_answer()).replace(' ', '')
        game.finish_game()
        if str(message.text) == str(answer):
            await bot.send_message(chat_id, 'Ух ты, верно!')
            await logic.upgrade_user_level(bot, chat_id, 100, game.difficulty)
            await logic.print_level(bot, chat_id)
        else:
            await bot.send_message(chat_id, 'Вам стоит еще потренироваться')
            await logic.upgrade_user_level(bot, chat_id, 0, 0)
            await logic.print_level(bot, chat_id)
        keyboard = logic.Markup().pull([emojize(':repeat_button: Еще раз'), emojize(':scroll: Выбрать режим')],
                                       'end_numbers_game')
        await bot.send_message(chat_id, 'Чем бы вы хотели заняться дальше?', reply_markup=keyboard)
    elif whats_game == config.words_answers:
        game = logic.MindGame(bot, message, config.words_answers, logic.get_difficulty(chat_id))
        answer = game.get_answer()
        game.finish_game()
        if str(message.text).lower() == str(answer):
            await bot.send_message(chat_id, 'Ух ты, верно!')
            await logic.upgrade_user_level(bot, chat_id, 100, game.difficulty)
            await logic.print_level(bot, chat_id)
        else:
            await bot.send_message(chat_id, 'Вам стоит еще потренироваться')
            await logic.upgrade_user_level(bot, chat_id, 0, 0)
            await logic.print_level(bot, chat_id)
        keyboard = logic.Markup().pull([emojize(':repeat_button: Еще раз'), emojize(':scroll: Выбрать режим')],
                                       'end_words_game')
        await bot.send_message(chat_id, 'Чем бы вы хотели заняться дальше?', reply_markup=keyboard)


#
#   Запуск бота на поллинг
# ыыы

if __name__ == '__main__':
    executor.start_polling(dp)

