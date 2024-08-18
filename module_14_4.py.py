from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import crud_functions


api = "7429366363:AAHxWZzj-M-sypwgulHAZ4i-rQWGpUGcg7w"
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

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(("Привет! Я бот, помогающий твоему здоровью.\n"
                          "Для начала введите 'Рассчитать'"), reply_markup=kb)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()

@dp.message_handler(lambda message: message.text == 'Рассчитать')
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=inline_kb)


@dp.message_handler(text=['Купить'])
async def get_buying_list(message: types.Message):
    products = crud_functions.get_all_products()
    for product in products:
        product_id, title, description, price, image_path = product
        with open(image_path, 'rb') as image:
            await message.answer_photo(image, caption=f'Название: {title} | Описание: {description} | Цена: {price} руб.')
    await message.answer('Выберите продукт для покупки:', reply_markup=product_inline_kb)

@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formula_message = (
        "Формула расчета калорий (Миффлин-Сан Жеор):\n"
        "Для мужчин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (годы) + 5\n"
        "Для женщин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (годы) - 161"
    )
    await call.message.answer(formula_message)

@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_gender(call: types.CallbackQuery):
    await UserState.gender.set()
    await call.message.answer("Введите свой пол (мужской/женский):")

@dp.callback_query_handler(lambda call: call.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Вы успешно приобрели продукт!")

@dp.message_handler(state=UserState.gender)
async def set_age(message: types.Message, state: FSMContext):
    if message.text.lower() in ['мужской', 'женский']:
        await state.update_data(gender=message.text.lower())
        await UserState.age.set()
        await message.answer('Введите свой возраст:')
    else:
        await message.answer("Пожалуйста, введите 'мужской' или 'женский'.")

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)

    await UserState.growth.set()
    await message.answer('Введите свой рост (в см):')


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer('Введите свой вес (в кг):')


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
