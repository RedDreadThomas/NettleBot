import logic
import time
import config
from emoji import emojize
from misc import dp, bot


async def starter_words_game(call, difficulty):
    """
    Эта функция запускает игру: Странные буквы
    :param call: (types.CallbackQuery)
    :param difficulty:
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':thumbs_up: Да!'), emojize(':scroll: Вернуться к выбору режима')],
                                   'words_game')
    await call.message.answer(f"Постарайтесь запомнить последовательность букв ниже за {10 * difficulty} секунд. "
                              "Для наибольшей эффективности, начинайте вводить ответ "
                              "после того, как они исчезнут. Готовы?", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'mind_game2' or c.data == 'end_words_game1')
async def words_game(call):
    """
    Эта функция запускает выбор сложности в игре Странные буквы
    :param call: (types.CallbackQuery)
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':pleading_face: Легко'), emojize(':grimacing_face: Нормально'),
                                    emojize(':skull_and_сrossbones: Сложно')], 'words_difficulty')
    await call.message.answer("Выберите уровень сложности", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'words_difficulty1' or c.data == 'words_difficulty2'
                                     or c.data == 'words_difficulty3')
async def choose_dif_strange_letters_game(call):
    """
    Эта функция запускает игру Странные буквы на выбранной сложности
    :param call: (types.CallbackQuery)
    :return:
    """
    chat_id = call.message.chat.id
    logic.add_difficulty(chat_id, int(call.data[-1]))
    await starter_words_game(call, int(call.data[-1]))


@dp.callback_query_handler(lambda c: c.data == "words_game1")
async def main_action_of_strange_letters_game(call):
    """
    Эта функция продолжает игру: Странные буквы
    :param call: (types.CallbackQuery)
    :return:
    """
    chat_id = call.message.chat.id
    difficulty = logic.get_difficulty(chat_id)
    types_of_difficulty = ['Низкая', 'Средняя', 'Высокая']
    strange_letters_game = logic.MindGame(bot, call.message, config.words_answers, difficulty)
    strange_letters_game.add_user_to_players()
    strange_letters = strange_letters_game.get_answer()
    strange_letters_message = await call.message.answer(f'Сложность {types_of_difficulty[difficulty - 1]}:'
                                                        f'\n{strange_letters}')
    time.sleep(10 * difficulty)
    await strange_letters_message.delete()
    await call.message.answer('Введите последовательность:')

