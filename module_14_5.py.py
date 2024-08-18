from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import crud_functions

api = "YOUR API"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button_buy = KeyboardButton(text='Купить')
kb.add(button, button2, button_buy)


inline_kb = InlineKeyboardMarkup()
button_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.add(button_calories, button_formulas)


product_inline_kb = InlineKeyboardMarkup()
button_product1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button_product2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button_product3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button_product4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
product_inline_kb.add(button_product1, button_product2, button_product3, button_product4)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button_buy = KeyboardButton(text='Купить')
button_register = KeyboardButton(text='Регистрация')  
kb.add(button, button2, button_buy, button_register)



class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(("Привет! Я бот, помогающий твоему здоровью.\n"
                          "Для начала введите 'Рассчитать'"), reply_markup=kb)


@dp.message_handler(lambda message: message.text == 'Регистрация')
async def sign_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()  # Переход к состоянию username


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if crud_functions.is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age = message.text
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')

    crud_functions.add_user(username, email, age)
    await message.answer(f"Регистрация завершена! Добро пожаловать, {username}.")
    await state.finish()


@dp.message_handler(lambda message: message.text == 'Рассчитать')
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=inline_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
