import random
import shelve
import config
from aiogram import types
import time


async def upgrade_user_level(message, exp=0, difficulty=0):
    """
    Эта функция обновляет опыт пользователя, повышает его уровень
    :param message:
    :param difficulty:
    :param exp: количество опыта, начисляемое пользователю
    :return: None
    """
    chat_id = message.chat.id
    now_exp = shelve.open(config.shelve_now_exp)
    max_exp = shelve.open(config.shelve_max_exp)
    level = shelve.open(config.shelve_usr_level)
    try:
        now_exp[str(chat_id)] += exp * difficulty
    except KeyError:
        now_exp[str(chat_id)] = exp * difficulty
        max_exp[str(chat_id)] = 200
        level[str(chat_id)] = 1
    await message.answer(f"Вы заработали {exp * difficulty} опыта")
    if max_exp[str(chat_id)] <= now_exp[str(chat_id)]:
        now_exp[str(chat_id)] -= max_exp[str(chat_id)]
        max_exp[str(chat_id)] *= 2
        level[str(chat_id)] += 1
        await message.answer("Поздравляем, ваш уровень повышен!")
    now_exp.close()
    max_exp.close()
    level.close()


async def print_level(message):
    """
    Эта функция отправляет актуальную информацию об уровне пользователя в чат
    :return: None
    """
    chat_id = message.chat.id
    now_exp = shelve.open(config.shelve_now_exp)
    max_exp = shelve.open(config.shelve_max_exp)
    level = shelve.open(config.shelve_usr_level)
    await message.answer(f"Уровень: {level[str(chat_id)]}\n{now_exp[str(chat_id)]}"
                                    f" опыта/{max_exp[str(chat_id)]} опыта")


# Функции отвечаюшие за выбор и хранение сложности игры


def add_difficulty(chat_id, difficulty):
    """
    Эта функция добавляет уровень сложности в config.shelve_difficulty
    :param chat_id:
    :param difficulty:
    :return:
    """
    with shelve.open(config.shelve_difficulty) as storage:
        storage[str(chat_id)] = difficulty


def get_difficulty(chat_id):
    """
    Эта функция возвращает уровень сложности из config.shelve_difficulty
    :param chat_id:
    :return:
    """
    with shelve.open(config.shelve_difficulty) as storage:
        return storage[str(chat_id)]


def del_difficulty(chat_id):
    """
    Эта функция удаляет уровень сложности из config.shelve_difficulty
    :param chat_id:
    :return:
    """
    with shelve.open(config.shelve_difficulty) as storage:
        del storage[str(chat_id)]


# Функции отвечаюшие за генерацию ответов


def alpha(n):
    """
    Эта функция генерирует последовательность букв
    :param n: (int) количество букв
    :return: (str) последовательность букв
    """
    return ''.join([chr(random.randint(1072, 1103)) for i in range(n)])


def pyramid(c_str):
    """
    Эта функция генерирует пирамидку из чисел
    :param c_str: (int) количество рядов в пирамиде
    :return: (str) пирамидка из чисел
    """
    list_strings = []
    count = c_str * 2 + 1
    for i in range(1, c_str + 1):
        items = list([str(random.randint(0, 9)) for _ in range(i)])
        s = ' '.join(items)
        spaces = ' ' * (count - len(s) // 2)
        list_strings.append("{}{}{}".format(spaces, s, spaces))
    return list_strings


def intervals_gen(mod):
    if mod == 0:
        return [1, 5, 15, 30]
    return [10, 60, 120]


# Модуль отвечающий за создание кастомных InlineKeyboardMarkup


class Markup:

    def __init__(self):
        self.markdown = types.InlineKeyboardMarkup()

    def pull(self, button_names, button_data):
        """
        Этот метод заполняет InlineKeyboard по заданым параметрам
        :param button_names: (list)  Список с текстом, который будет на кнопках
        :param button_data: (str) Строка, которая будет служить шаблоном для callback_data
        :return: (types.InlineKeyboardMarkup) Заполненая кнопками клавиатура
        """
        counter = 1
        for name in button_names:
            button = types.InlineKeyboardButton(text=name, callback_data=f'{button_data}{counter}')
            self.markdown.add(button)
            counter += 1
        return self.markdown


# Модуль отвечающий за развивающие игры


class BotMod:

    def __init__(self, message, session_name, mod=0):
        """
        Этот метод создает экземпляр игры
        :param message:
        :param session_name: (str) Строка, содержащая в себе название файла с ответами("numbers.db", "words.db")
        или название режима("search")
        """
        self.chat_id = message.chat.id
        self.message = message
        self.session_name = session_name
        self.mod = mod

    def generate(self):
        """
        Этот метод генерирует последовательности или возвращает название запущенного режима
        в зависимости от self.mod_name
        :return: при self.mode_name = 'search' -> Название запущенной сессии
                 при self.mode_name = названию файла-хранилища -> Сгенерированное значение
        """
        if self.session_name == config.numbers_answers:
            return pyramid(int(4 * self.mod) - self.mod)
        elif self.session_name == config.words_answers:
            return alpha(int(8 * self.mod))

    def add_user_to_storage(self):
        """
        Этот метод добавляет id игрока в файл shelve.db
        :return: None
        """
        if self.session_name == config.shelve_reminders_dates:
            now_datetime = int(time.time())
            with shelve.open(config.shelve_reminders_dates) as storage:
                try:
                    storage[str(self.chat_id)] += str(now_datetime) + ' '
                except KeyError:
                    storage[str(self.chat_id)] = str(now_datetime) + ' '
        elif self.session_name == config.shelve_reminders_levels:
            with shelve.open(config.shelve_reminders_levels) as storage:
                try:
                    storage[str(self.chat_id)] += '0 '
                except KeyError:
                    storage[str(self.chat_id)] = '0 '
        elif self.session_name == config.shelve_reminders:
            reminder = self.message.text.replace(' ', '!@$%^&*()_+')
            with shelve.open(config.shelve_reminders) as storage:
                try:
                    storage[str(self.chat_id)] += f'{reminder} '
                except KeyError:
                    storage[str(self.chat_id)] = f'{reminder} '
        elif self.session_name == config.shelve_reminders_mods:
            with shelve.open(config.shelve_reminders_mods) as storage:
                try:
                    storage[str(self.chat_id)] += f'{self.mod - 1} '
                except KeyError:
                    storage[str(self.chat_id)] = f'{self.mod - 1} '

        else:
            with shelve.open(self.session_name) as storage:
                storage[str(self.chat_id)] = self.generate()

    def user_in_storage(self):
        with shelve.open(self.session_name) as storage:
            return str(self.chat_id) in storage

    def get_answer(self):
        """
        Этот метод проверяет, участвует ли пользователь в игре
        :return: None или правильный ответ в игре
        Можно переделать, чтобы не захламлять self.generate() проверкой
        """

        with shelve.open(self.session_name) as storage:
            try:
                answer = storage[str(self.chat_id)]
                return answer
            except KeyError:
                return None

    def finish_session(self):
        """
        Этот метод удаляет id пользователя из хранилища с ответами
        :return: None
        """
        with shelve.open(self.session_name) as storage:
            try:
                del storage[str(self.chat_id)]
            except KeyError:
                pass
        with shelve.open(config.shelve_difficulty) as storage:
            try:
                del storage[str(self.chat_id)]
            except KeyError:
                pass
