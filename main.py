import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = '8517647989:AAFvw2mId7wMmJ8X91IZan-AYZwgh5mEaAk'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

user_tasks = {}

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Сделать заказ')],
        [KeyboardButton(text='Мои заказы')],
        [KeyboardButton(text="Очистить заказы")]
    ],
    resize_keyboard=True
)

class Order(StatesGroup):  
    name = State()
    product = State()
    time = State()

@dp.message(Command('basket'))
async def basket(message: types.Message):
    await message.answer("Корзина для заказов", reply_markup=keyboard)

@dp.message(Command('todo'))
async def todo(message: types.Message):
    await message.answer("TODO", reply_markup=keyboard)

@dp.message(lambda msg: msg.text == "Сделать заказ")
async def start_order(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(Order.name)

@dp.message(Order.name)
async def order_name(message: types.Message, state: FSMContext): 
    await state.update_data(name=message.text)
    await message.answer("Что вы хотите заказать?")
    await state.set_state(Order.product)


@dp.message(Order.product)
async def order_product(message: types.Message, state: FSMContext):  
    await state.update_data(product=message.text) 
    await message.answer("К какому времени привезти заказ?")
    await state.set_state(Order.time)

@dp.message(Order.time)
async def order_time(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    user_tasks.setdefault(user_id, [])
    user_tasks[user_id].append({
        "name": data["name"],
        "product": data["product"],
        "time": message.text
    })

    await message.answer(
        f"✅ Заказ принят!\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📦 Заказ: {data['product']}\n"
        f"⏰ Время: {message.text}"
    )

    await state.clear()

@dp.message(lambda msg: msg.text == "Мои заказы")
async def my_orders(message: types.Message):
    orders = user_tasks.get(message.from_user.id)

    if not orders:
        await message.answer("У вас нет заказов 😕")
        return

    text = "📋 Ваши заказы:\n\n"
    for i, order in enumerate(orders, 1):
        text += (
            f"{i}. 👤 {order['name']}\n"
            f"   📦 {order['product']}\n"
            f"   ⏰ {order['time']}\n\n"
        )

    await message.answer(text)

@dp.message(lambda msg: msg.text == "Очистить заказы")
async def clear_tasks(message: types.Message):
    user_tasks[message.from_user.id] = []
    await message.answer("🗑 Все заказы удалены")

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет! Я твой новый бот 😎", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# import asyncio
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.memory import MemoryStorage

# API_TOKEN = '8517647989:AAFvw2mId7wMmJ8X91IZan-AYZwgh5mEaAk'

# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()

# user_tasks = {}

# keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='Сделать заказ')],
#         [KeyboardButton(text='Мои заказы')],
#         [KeyboardButton(text="Очистить заказы")]
#     ],
#     resize_keyboard=True
# )

# class order(StatesGroup):
#     name = State()
#     product = State ()
#     time = State()

# @dp.message(Command('basket'))
# async def basket(message: types.Message):
#     await message.answer("Корзина для заказов", reply_markup=keyboard)

# @dp.message(Command('todo'))
# async def todo(message: types.Message):
#     await message.answer("TODO", reply_markup=keyboard)

# @dp.message(lambda msg: msg.text == "Сделать заказ")
# async def start_order(message: types.Message, state: FSMContext):
#     await message.answer("как вас зовут?")
#     await state.set_state(order.name)
    
# @dp.message(order.name)
# async def order_name(message: types.Message, state: FSMContext): 
#     await state.update_data(name=message.text)
#     await message.answer("Что вы хотите заказать?")
#     await state.set_state(order.product)
    
# @dp.message(order.product)
# async def order_name(message: types.Message, state: FSMContext): 
#     await state.update_data(name=message.text)
#     await message.answer("К какому времени привезти заказ?")
#     await state.set_state(order.time)
   
# @dp.message(order.time)
# async def order_time(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     user_id = message.from_user.id

#     user_tasks.setdefault(user_id, [])
#     user_tasks[user_id].append({
#         "name": data["name"],
#         "product": data["product"],
#         "time": message.text
#     })

#     await message.answer(
#         f"✅ Заказ принят!\n\n"
#         f"👤 Имя: {data['name']}\n"
#         f"📦 Заказ: {data['product']}\n"
#         f"⏰ Время: {message.text}"
#     )

#     await state.clear()

# @dp.message(lambda msg: msg.text == "Мои заказы")
# async def my_orders(message: types.Message):
#     orders = user_tasks.get(message.from_user.id)

#     if not orders:
#         await message.answer("У вас нет заказов 😕")
#         return

#     text = "📋 Ваши заказы:\n\n"
#     for i, order in enumerate(orders, 1):
#         text += (
#             f"{i}. 👤 {order['name']}\n"
#             f"   📦 {order['product']}\n"
#             f"   ⏰ {order['time']}\n\n"
#         )

#     await message.answer(text)

# @dp.message(lambda msg: msg.text == "Очистить заказы")
# async def clear_tasks(message: types.Message):
#     user_tasks[message.from_user.id] = []
#     await message.answer("🗑 Все заказы удалены")

# @dp.message(Command('start'))
# async def start(message: types.Message):
#     await message.answer("Привет! я твой новый бот😎", reply_markup=keyboard)  

# async def main():
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     asyncio.run(main())
   
   
# @dp.message(Command('start'))
# async def start(message: types.Message):
#     await message.answer("Привет! я твой новый бот😎", reply_markup=keyboard)  
    
    
    

# @dp.message(lambda msg: msg.text not in ['Сделать заказ', 'Очистить заказы', 'Добавить заказ'] 
#             and not msg.text.startswith('/'))
# async def save_task(message: types.Message):
#     user_id = message.from_user.id
#     user_tasks.setdefault(user_id, [])
#     user_tasks[user_id].append(message.text)
#     await message.answer(f"Заказ добавлен:\n{message.text}")
    
# @dp.message(lambda msg: msg.text == "")
# async def clear_tasks(message: types.Message):
#     user_tasks[message.from_user.id] = []
#     await message.answer("Все заказы удалены")
    
    


# @dp.message(lambda msg: msg.text == "Очистить заказы")
# async def clear_tasks(message: types.Message):
#     user_tasks[message.from_user.id] = []
#     await message.answer("Все заказы удалены")

# @dp.message(Command('start'))
# async def start(message: types.Message):
#     await message.answer("Привет! я твой новый бот😎", reply_markup=keyboard)

# # Общий echo ставится СТРОГО последним
# @dp.message()
# async def echo_last(message: types.Message):
#     await message.answer(f"Ты написал {message.text}")


# async def main():
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#     asyncio.run(main())  