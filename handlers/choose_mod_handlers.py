import logic
import time
from handlers.main_menu_handlers import menu_command
from misc import dp
from emoji import emojize
from aiogram import types


@dp.callback_query_handler(lambda c: c.data == 'menu1')
async def choose_game(call: types.CallbackQuery):
    """
    Эта функция отправляет сообщение с выбором игры
    :param call: (types.CallbackQuery)
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':input_numbers: Пирамидка'),
                                    emojize(':input_latin_lowercase: Странные буквы'),
                                    emojize(':scroll: Вернуться к выбору режима')], 'mind_game')
    await call.message.answer('Выберите один из режимов', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'menu2')
async def remember_new(call: types.CallbackQuery):
    """
    Эта функция пока находится в разработке, поэтому пока что отправляет сообщение о том, что находится в разработке
    :param call: (types.CallbackQuery)
    :return:
    """
    keyboard = logic.Markup().pull(['Быстро', 'Надолго', 'Текущая тема'], 'remember_mod')
    await call.message.answer('Выберите режим запоминания:', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'menu3')
async def repeat_old(call: types.CallbackQuery):
    """
     Эта функция пока находится в разработке, поэтому пока что отправляет сообщение о том, что находится в разработке
    :param call: (types.CallbackQuery)
    :return:
    """
    informer_message = await call.message.answer('Эта функция пока находится в разработке. Мы скоро все '
                                                 'доделаем <3')
    time.sleep(2)
    await informer_message.delete()


@dp.callback_query_handler(lambda c: c.data == 'menu4' or c.data == 'exit_from_info1'
                                     or c.data == 'exit_from_communication1', state="*")
async def main_menu(call: types.CallbackQuery):
    """
    Эта функция возвращает пользователя в главное меню
    :param call: (types.CallbackQuery)
    :return:
    """
    await menu_command(call.message)
