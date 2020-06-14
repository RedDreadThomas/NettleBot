import random
import shelve
import config
from aiogram import types
import time


async def upgrade_user_level(bot, chat_id, exp, difficulty):
    """
    Эта функция обновляет опыт пользователя, повышает его уровень
    :param difficulty:
    :param bot: (aiogram.Bot)
    :param chat_id: Айди чата с пользователем
    :param exp: количество опыта, начисляемое пользователю
    :return: None
    """
    now_exp = shelve.open(config.shelve_now_exp)
    max_exp = shelve.open(config.shelve_max_exp)
    level = shelve.open(config.shelve_usr_level)
    try:
        now_exp[str(chat_id)] += exp * difficulty
    except KeyError:
        now_exp[str(chat_id)] = exp * difficulty
        max_exp[str(chat_id)] = 200
        level[str(chat_id)] = 1
    await bot.send_message(chat_id,
                           f"Вы заработали {exp * difficulty} опыта")
    if max_exp[str(chat_id)] <= now_exp[str(chat_id)]:
        now_exp[str(chat_id)] -= max_exp[str(chat_id)]
        max_exp[str(chat_id)] *= 2
        level[str(chat_id)] += 1
        await bot.send_message(chat_id,
                               "Поздравляем, ваш уровень повышен!")
    now_exp.close()
    max_exp.close()
    level.close()


async def print_level(bot, chat_id):
    """
    Эта функция отправляет актуальную информацию об уровне пользователя в чат
    :param bot: (aiogram.Bot)
    :param chat_id: Айди чата с пользователем
    :return: None
    """
    now_exp = shelve.open(config.shelve_now_exp)
    max_exp = shelve.open(config.shelve_max_exp)
    level = shelve.open(config.shelve_usr_level)
    await bot.send_message(chat_id, f"Уровень: {level[str(chat_id)]}\n{now_exp[str(chat_id)]}"
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


class MindGame:

    def __init__(self, bot, message, mod_name, difficulty=0):
        """
        Этот метод создает экземпляр игры
        :param bot: (aiogram.Bot)
        :param message:
        :param mod_name: (str) Строка, содержащая в себе название файла с ответами("numbers.db", "words.db")
        или название режима("search")
        """
        self.chat_id = message.chat.id
        self.bot = bot
        self.message_id = message.message_id
        self.mod_name = mod_name
        self.difficulty = difficulty

    def generate(self):
        """
        Этот метод генерирует последовательности или возвращает название запущенного режима
        в зависимости от self.mod_name
        :return: при self.mode_name = 'search' -> Название запущенной сессии
                 при self.mode_name = названию файла-хранилища -> Сгенерированное значение
        """
        if self.mod_name == config.numbers_answers:
            return pyramid(int(3 * self.difficulty))
        elif self.mod_name == config.words_answers:
            return alpha(int(10 * self.difficulty))
        elif self.mod_name == config.shelve_date:
            now_datetime = int(time.time())
            return now_datetime
        elif self.mod_name == config.shelve_lvl_of_reminders:
            return 0
        elif self.mod_name == 'search':
            for db in config.list_shelve_answers:
                try:
                    storage = shelve.open(db)
                    test_eq = storage[str(self.chat_id)]
                    return db
                except KeyError:
                    pass

    def add_user_to_players(self):
        """
        Этот метод добавляет id игрока в файл shelve.db
        :return: None
        """
        with shelve.open(self.mod_name) as storage:
            storage[str(self.chat_id)] = self.generate()

    def user_in_players(self):
        with shelve.open(self.mod_name) as storage:
            return str(self.chat_id) in storage

    def get_answer(self):
        """
        Этот метод проверяет, участвует ли пользователь в игре
        :return: None или правильный ответ в игре
        Можно переделать, чтобы не захламлять self.generate() проверкой
        """

        with shelve.open(self.mod_name) as storage:
            try:
                answer = storage[str(self.chat_id)]
                return answer
            except KeyError:
                return None

    def finish_game(self):
        """
        Этот метод удаляет id пользователя из хранилища с ответами
        :return: None
        """
        with shelve.open(self.mod_name) as storage:
            try:
                del storage[str(self.chat_id)]
            except KeyError:
                pass
        with shelve.open(config.shelve_difficulty) as storage:
            try:
                del storage[str(self.chat_id)]
            except KeyError:
                pass
