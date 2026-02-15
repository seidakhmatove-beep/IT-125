import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import Database

class RegSteps(StatesGroup):
    full_name = State()
    age = State()
    group_code = State()
    phone = State()
    email = State()
    tg_username = State()
    hobby = State()
    fav_subject = State()
    hometown = State()
    motivation = State()

bot = Bot(token="8578909579:AAEbELwF2V3gzXlQxIdtdJoRg860mnFVAmM")
dp = Dispatcher()
db = Database("university.db")


@dp.message(Command("start"))
async def start_reg(message: types.Message, state: FSMContext):
    await message.answer("Привет! Давай зарегистрируем тебя в базе одногруппников.\nВведите ФИО:")
    await state.set_state(RegSteps.full_name)

@dp.message(RegSteps.full_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(RegSteps.age)

@dp.message(RegSteps.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Твой номер группы?")
    await state.set_state(RegSteps.group_code)

@dp.message(RegSteps.group_code)
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(group_code=message.text)
    await message.answer("Твой номер телефона?")
    await state.set_state(RegSteps.phone)

@dp.message(RegSteps.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Твой Email?")
    await state.set_state(RegSteps.email)

@dp.message(RegSteps.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Твой ник в Telegram (через @)?")
    await state.set_state(RegSteps.tg_username)

@dp.message(RegSteps.tg_username)
async def process_tg(message: types.Message, state: FSMContext):
    await state.update_data(tg_username=message.text)
    await message.answer("Твоё хобби?")
    await state.set_state(RegSteps.hobby)

@dp.message(RegSteps.hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    await state.update_data(hobby=message.text)
    await message.answer("Любимый предмет?")
    await state.set_state(RegSteps.fav_subject)

@dp.message(RegSteps.fav_subject)
async def process_subject(message: types.Message, state: FSMContext):
    await state.update_data(fav_subject=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(RegSteps.hometown)

@dp.message(RegSteps.hometown)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(hometown=message.text)
    await message.answer("Почему ты выбрал это направление обучения?")
    await state.set_state(RegSteps.motivation)

@dp.message(RegSteps.motivation)
async def finish_reg(message: types.Message, state: FSMContext):
    await state.update_data(motivation=message.text)

    user_data = await state.get_data()

    db.add_classmate(message.from_user.id, user_data)

    await message.answer("Регистрация завершена! Твои данные сохранены в SQLite.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())