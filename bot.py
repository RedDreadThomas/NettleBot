#! /usr/bin/python3.7
# -*- coding = utf-8 -*-
import handlers
from aiogram.utils import executor
from misc import dp

if __name__ == '__main__':
    executor.start_polling(dp)

