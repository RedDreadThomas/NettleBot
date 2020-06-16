import logic
import config
import time
from aiogram import types
from misc import dp
from emoji import emojize
from handlers.states import NettleBot


async def starter_numbers_game(call: types.CallbackQuery, difficulty):
    """
    Эта функция запускает игру: Пирамидка
    :param call: (types.CallbackQuery)
    :param difficulty:
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':thumbs_up: Да!'), emojize(':scroll: Вернуться к выбору режима')],
                                   'numbers_game')
    await call.message.answer(f"Постарайтесь запомнить все цифры ниже за {10 * difficulty} секунд. "
                               "Для наибольшей эффективности, начинайте вводить ответ "
                               "после того, как они исчезнут. Готовы?", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'mind_game1' or c.data == 'end_numbers_game1')
async def pyramid_game(call: types.CallbackQuery):
    """
    Эта функция запускает выбор сложности игры: Пирамидка
    :param call: (types.CallbackQuery)
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':pleading_face: Легко'), emojize(':grimacing_face: Нормально'),
                                    emojize(':skull_and_crossbones: Сложно')], 'num_difficulty')
    await call.message.answer("Выберите уровень сложности", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'num_difficulty1' or c.data == 'num_difficulty2'
                           or c.data == 'num_difficulty3')
async def choose_dif_pyramid_game(call: types.CallbackQuery):
    """
    Эта функция запускает игру Пирамидка на выбранной сложности
    :param call: (types.CallbackQuery)
    :return:
    """
    chat_id = call.message.chat.id
    logic.add_difficulty(chat_id, int(call.data[-1]))
    await starter_numbers_game(call, int(call.data[-1]))


@dp.callback_query_handler(lambda c: c.data == "numbers_game1")
async def main_action_of_pyramid_game(call: types.CallbackQuery):
    """
    Эта функция продолжает игру: Пирамидка
    :param call: (types.CallbackQuery)
    :return:
    """
    chat_id = call.message.chat.id
    difficulty = logic.get_difficulty(chat_id)
    types_of_difficulty = ['Низкая', 'Средняя', 'Высокая']
    numbers_game = logic.BotMod(call.message, config.numbers_answers, difficulty)
    numbers_game.add_user_to_storage()
    pyramid = "\n".join(numbers_game.get_answer())
    pyramid_message = await call.message.answer(f'Сложность {types_of_difficulty[difficulty - 1]}:\n{pyramid}')
    time.sleep(10 * difficulty)
    await pyramid_message.delete()
    await call.message.answer('Введите последовательность:')
    await NettleBot.waiting_for_answer_in_pyramid_game.set()


@dp.message_handler(state=NettleBot.waiting_for_answer_in_pyramid_game, content_types=types.ContentTypes.TEXT)
async def checker_for_answer_in_pyramid_game(message, state):
    await state.finish()
    chat_id = message.chat.id
    game = logic.BotMod(message, config.numbers_answers, logic.get_difficulty(chat_id))
    answer = ''.join(game.get_answer()).replace(' ', '')
    game.finish_session()
    if str(message.text) == str(answer):
        await message.answer('Ух ты, верно!')
        await logic.upgrade_user_level(message, 100, game.mod)
        await logic.print_level(message)
    else:
        await message.answer('Вам стоит еще потренироваться')
        await logic.upgrade_user_level(message)
        await logic.print_level(message)
    keyboard = logic.Markup().pull([emojize(':repeat_button: Еще раз'), emojize(':scroll: Выбрать режим')],
                                   'end_numbers_game')
    await message.answer('Чем бы вы хотели заняться дальше?', reply_markup=keyboard)
