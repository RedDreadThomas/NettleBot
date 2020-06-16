from aiogram.dispatcher.filters.state import StatesGroup, State


class NettleBot(StatesGroup):
    waiting_for_choose_mod = State()
    waiting_for_choose_game_mod = State()

    waiting_for_choose_difficulty_pyramid_game = State()
    waiting_for_start_pyramid_game = State()
    waiting_for_answer_in_pyramid_game = State()

    waiting_for_choose_difficulty_strange_letters_game = State()
    waiting_for_start_strange_letters_game = State()
    waiting_for_answer_in_strange_letters_game = State()

    waiting_for_name_in_remembers_new_mod = State()
