import logic
from aiogram import types
from misc import dp
from emoji import emojize


@dp.message_handler(commands=['menu'])
async def menu_command(message: types.Message):
    """
    Эта функция отправляет пользователю сообщение с главным меню
    :param message: (types.Message)
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':scroll: Выбрать режим'), emojize(':books: Информация'),
                                    emojize(':telephone_receiver: Связаться с нами')], 'main_menu')
    await message.answer("Главное меню:", reply_markup=keyboard)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """
    Эта функция отправляет приветсвие и знакомит пользователя с основными функциями бота,
    а также отправляет пользователю сообщение с главным меню
    :param message: (types.Message)
    :return:
    """
    await message.answer('Приветствуем вас в боте "Крапивка Помнит"! '
                         'Этот бот создан для того, чтобы помогать вам '
                         'развивать память, не забывать повторять пройденный '
                         'материал и лучше понимать изучаемые темы.')
    await menu_command(message)


@dp.callback_query_handler(
    lambda c: c.data == 'main_menu1'
    or c.data == 'mind_game3'
    or c.data == 'words_game2'
    or c.data == 'numbers_game2'
)
async def choose_mod(call: types.CallbackQuery):
    """
    Эта функция отправляет пользователю сообщение с выбором режимов
    :param call: (types.CallbackQuery)
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':brain: Развить память'), emojize(':graduation_cap: Запомнить новое'),
                                    emojize(':no_entry: Повторить старое'), emojize(':left_arrow: Назад')],
                                   'menu')
    await call.message.edit_text('Выберите один из режимов бота, краткое описание каждого из нх вы можете найти в'
                                 'разделе "Информация" главного меню.', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'main_menu2')
async def information(call: types.CallbackQuery):
    """
    Эта функция отправляет пользователю сообщение с информацией о возможностях бота
    :param call: (types.CallbackQuery)
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':left_arrow: Назад')], 'exit_from_info')
    await call.message.edit_text("Крапивка будет способна работать в 3 режимах:\n"
                                 "1)Развить память.\n"
                                 "В этом режиме вам будет предложено сыграть в игры, "
                                 "которые способствуют улучшению памяти\n"
                                 "2)Запомнить новое.\n"
                                 "Этот режим пока находится в разработке."
                                 "Основная цель этого режима - спланировать режим повторения"
                                 " изучаемой темы и напоминать вам, когда стоит к ней вернуться."
                                 "График составляется с помощью кривой Эббингауза.\n"
                                 "3)Повторить старое.\n"
                                 "Этот режим пока находится в разработке."
                                 "Основная цель этого режима - помочь глубже понять изучаемую"
                                 " тему. Для достижения результата, бот будет использовать"
                                 " метод Фейнмана.", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'main_menu3')
async def callback(call: types.CallbackQuery):
    """
    Эта функция отправляет сообщение со способами связи с разработчиком
    :param call: (types.CallbackQuery)
    :return:
    """
    keyboard = logic.Markup().pull([emojize(':left_arrow: Назад')], 'exit_from_communication')
    await call.message.edit_text("Если у вас есть предложения или жалобы, можете смело писать нам:\n"
                                 "На почту: скоро\n"
                                 "В группу в Вк: скоро\n"
                                 "В телеграм: @RdddTms или @innagvozdika.", reply_markup=keyboard)
