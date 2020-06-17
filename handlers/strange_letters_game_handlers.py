import logic
import time
import config
from aiogram.dispatcher import FSMContext
from emoji import emojize
from misc import dp
from aiogram import types
from handlers.states import NettleBot


async def starter_words_game(call, difficulty):
    """
    Эта функция запускает игру: Странные буквы
    :param call: (types.CallbackQuery)
    :param difficulty:
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':thumbs_up: Да!'), emojize(':left_arrow: Назад')],
                                   'words_game')
    await call.message.answer(f"Постарайтесь запомнить последовательность букв ниже за {10 * difficulty} секунд. "
                              "Для наибольшей эффективности, начинайте вводить ответ "
                              "после того, как они исчезнут. Готовы?", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'mind_game2' or c.data == 'end_words_game1')
async def words_game(call: types.CallbackQuery):
    """
    Эта функция запускает выбор сложности в игре Странные буквы
    :param call: (types.CallbackQuery)
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':pleading_face: Легко'), emojize(':grimacing_face: Нормально'),
                                    emojize(':skull_and_crossbones: Сложно')], 'words_difficulty')
    await call.message.edit_text("Выберите уровень сложности", reply_markup=keyboard)
    await NettleBot.waiting_for_choose_difficulty_in_strange_letters_game.set()


@dp.callback_query_handler(lambda c: c.data == 'words_difficulty1'
                           or c.data == 'words_difficulty2'
                           or c.data == 'words_difficulty3',
                           state=NettleBot.waiting_for_choose_difficulty_in_strange_letters_game)
async def choose_dif_strange_letters_game(call: types.CallbackQuery):
    """
    Эта функция запускает игру Странные буквы на выбранной сложности
    :param call: (types.CallbackQuery)
    :return:
    """
    chat_id = call.message.chat.id
    logic.add_difficulty(chat_id, int(call.data[-1]))
    await starter_words_game(call, int(call.data[-1]))
    await NettleBot.waiting_for_start_strange_letters_game.set()


@dp.callback_query_handler(lambda c: c.data == "words_game1",
                           state=NettleBot.waiting_for_start_strange_letters_game)
async def main_action_of_strange_letters_game(call: types.CallbackQuery):
    """
    Эта функция продолжает игру: Странные буквы
    :param call: (types.CallbackQuery)
    :return:
    """
    chat_id = call.message.chat.id
    difficulty = logic.get_difficulty(chat_id)
    types_of_difficulty = ['Низкая', 'Средняя', 'Высокая']
    strange_letters_game = logic.BotMod(call.message, config.words_answers, difficulty)
    strange_letters_game.add_user_to_storage()
    strange_letters = strange_letters_game.get_answer()
    strange_letters_message = await call.message.answer(f'Сложность {types_of_difficulty[difficulty - 1]}:'
                                                        f'\n{strange_letters}')
    time.sleep(10 * difficulty)
    await strange_letters_message.delete()
    await call.message.answer('Введите последовательность:')
    await NettleBot.waiting_for_answer_in_strange_letters_game.set()


@dp.message_handler(state=NettleBot.waiting_for_answer_in_strange_letters_game, content_types=types.ContentTypes.TEXT)
async def checker_for_answer_in_strange_letters_game(message: types.Message, state: FSMContext):
    await state.finish()
    chat_id = message.chat.id
    game = logic.BotMod(message, config.words_answers, logic.get_difficulty(chat_id))
    answer = game.get_answer()
    game.finish_session()
    if str(message.text).lower() == str(answer):
        await message.answer('Ух ты, верно!')
        await logic.upgrade_user_level(message, 100, game.mod)
        await logic.print_level(message)
    else:
        await message.answer('Вам стоит еще потренироваться')
        await logic.upgrade_user_level(message)
        await logic.print_level(message)
    keyboard = logic.Markup().pull([emojize(':repeat_button: Еще раз'), emojize(':scroll: Выбрать режим')],
                                   'end_words_game')
    await message.answer('Чем бы вы хотели заняться дальше?', reply_markup=keyboard)

