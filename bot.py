import logic
import config
import handlers
from aiogram import types
from aiogram.utils import executor
from emoji import emojize
from misc import dp, bot


@dp.message_handler(lambda message: True, content_types=["text"])
async def text_checker(message: types.Message):
    """
    Эта функция обрабатывает все текстовые сообщения и
    1) Удаляет спам
    2) Завершает игру(проверяет правильность ответа, обновляет уровень пользователя)
    :param message: (types.Message)
    :return:
    """
    chat_id = message.chat.id
    await bot.delete_message(chat_id, message.message_id)


#
#   Запуск бота на поллинг
# ыыы

if __name__ == '__main__':
    executor.start_polling(dp)

