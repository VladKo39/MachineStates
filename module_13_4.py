from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# Импорт классов State и StatesGroup из aiogram.dispatcher.filters.state.
import asyncio

''''''
key_file = 'key.txt'
# храню токен
with open(key_file, 'r', encoding='utf-8') as file:
    # читаю токен
    key_ = str(file.read().strip())
api = key_

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    '''
    UserState  для определения группы состояний пользователя в Telegram-боте
    Объекты класса State
    age возраст
    groth рост
    weght вес
    '''
    age: int = State()
    growth: int = State()
    weight: int = State()
    gender: str = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(f'Для начала работы наберите Calories')


@dp.message_handler(text=['Calories'])
# Обернунуть set_age(message) в message_handler,
# который реагирует на текстовое сообщение 'Calories'.
async def set_age(message):
    await message.answer('Введите свой возраст:')
    # @dp.message_handler выводит сообщение Telegram-бот
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
# Обернунуть set_age(message) в message_handler,
# который реагирует на текстовое сообщение
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Введите свой пол: муж / жен ')
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_gender(message, state):
    await state.update_data(gender=message.text)
    data_quest = await state.get_data()

    if data_quest['gender'] == 'муж':
        result = 10 * int(data_quest['weight']) + \
                 6.25 * int(data_quest['growth']) - \
                 5 * int(data_quest['age']) + 5
        gend = 'мужчин'

    elif data_quest['gender'] == 'жен':
        result = 10 * int(data_quest['weight']) + \
                 6.25 * int(data_quest['growth']) - \
                 5 * int(data_quest['age']) + 5
        10 * int(data_quest['weight']) + \
        6.25 * int(data_quest['growth']) - \
        5 * int(data_quest['age']) - 161
        gend = 'женщин'

    await message.answer(f'Ваша норма калорий: {result} ккал в сутки для {gend}')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
