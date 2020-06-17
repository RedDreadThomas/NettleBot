#! /usr/bin/python3.7
# -*- coding = utf-8 -*-
from misc import dp
from aiogram import types


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def deleter_of_spam(message: types.Message):
    await message.delete()
