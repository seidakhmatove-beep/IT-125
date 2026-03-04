import asyncio
import logging
import sqlite3
import re
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

TOKEN = '8578909579:AAEbELwF2V3gzXlQxIdtdJoRg860mnFVAmM'
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

def extract_number(text):
    """Вытаскивает только цифры из строки (чтобы '80 кг' стало 80)"""
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", text.replace(',', '.'))
    return float(nums[0]) if nums else None

def init_db():
    conn = sqlite3.connect('fitness_pro.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            goal TEXT,
            weight REAL,
            height INTEGER,
            age INTEGER,
            calories INTEGER,
            diet_type TEXT,
            reg_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            weight REAL,
            trainings INTEGER,
            diet_score INTEGER,
            sleep_avg REAL
        )
    ''')
    conn.commit()
    conn.close()

def db_save_user(u_id, name, goal, w, h, age, cal, diet):
    conn = sqlite3.connect('fitness_pro.db')
    cursor = conn.cursor()
    reg_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (u_id, name, goal, w, h, age, cal, diet, reg_date))
    conn.commit()
    conn.close()

def db_save_report(u_id, w, trains, diet_s, sleep):
    conn = sqlite3.connect('fitness_pro.db')
    cursor = conn.cursor()
    date_now = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO progress (user_id, date, weight, trainings, diet_score, sleep_avg)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (u_id, date_now, w, trains, diet_s, sleep))
    conn.commit()
    conn.close()

def db_get_profile(u_id):
    conn = sqlite3.connect('fitness_pro.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (u_id,))
    res = cursor.fetchone()
    conn.close()
    return res

def db_get_last_weight(u_id):
    conn = sqlite3.connect('fitness_pro.db')
    cursor = conn.cursor()
    cursor.execute('SELECT weight FROM progress WHERE user_id = ? ORDER BY id DESC LIMIT 1', (u_id,))
    res = cursor.fetchone()
    if not res:
        cursor.execute('SELECT weight FROM users WHERE user_id = ?', (u_id,))
        res = cursor.fetchone()
    conn.close()
    return res[0] if res else None

init_db()

DIETS = {
    "Мясоед": {
        "Завтрак": ["Омлет из 3 яиц с беконом", "Стейк из индейки с сыром", "Творог 9% с ягодами"],
        "Обед": ["Говядина на гриле + бурый рис", "Куриное филе + паста", "Котлеты из лося + гречка"],
        "Ужин": ["Лосось с брокколи", "Салат с тунцом и яйцом", "Шашлык из курицы + овощи"]
    },
    "Вегетарианец": {
        "Завтрак": ["Смузи с протеином и бананом", "Тост с авокадо и нутом", "Овсянка на миндальном молоке"],
        "Обед": ["Стейк из тофу + киноа", "Чечевичный суп-пюре", "Грибы в сливках с рисом"],
        "Ужин": ["Овощное рагу с фасолью", "Хумус с овощными палочками", "Греческий салат с фетой"]
    },
    "Фастфуд-лайф": {
        "Завтрак": ["Яичница с сосисками", "Блины с мясом", "Сэндвич с ветчиной"],
        "Обед": ["Домашний бургер (много мяса)", "Шаурма в лаваше", "Домашняя пицца"],
        "Ужин": ["Пельмени из говядины", "Сырники со сметаной", "Кефир и творожный сырок"]
    }
}

WORKOUTS = {
    "🔱 Путь Эстета (David Laid)": [
        "Становая тяга: 4х6 (Тяжело)", "Жим под углом: 4х10", "Махи гантелями: 5х15", "Тяга верхнего блока: 4х12"
    ],
    "🥩 Массонабор": [
        "Приседания со штангой: 3х8", "Жим штанги лежа: 4х8", "Армейский жим: 3х10", "Подъем на бицепс: 3х12"
    ],
    "🍏 Похудение": [
        "Берпи: 4х15", "Выпады с гантелями: 3х20", "Прыжки на скакалке: 3 мин", "Планка: 3х1 мин"
    ],
    "⚖️ Поддержание формы": [
        "Отжимания: 4х20", "Подтягивания: 3х10", "Приседания (свой вес): 3х30", "Бег: 20 мин"
    ]
}

class Registration(StatesGroup):
    goal = State()
    name = State()
    age = State()
    weight = State()
    height = State()
    train_days = State()
    diet_type = State()
    sleep_hours = State()

class WeeklyReport(StatesGroup):
    weight = State()
    trains = State()
    diet_score = State()
    sleep = State()

def get_main_kb():
    b = ReplyKeyboardBuilder()
    for t in ["🍏 Похудение", "🥩 Массонабор", "🔱 Путь Эстета (David Laid)", "⚖️ Поддержание"]: b.button(text=t)
    return b.adjust(2).as_markup(resize_keyboard=True)

def get_menu_kb():
    b = ReplyKeyboardBuilder()
    b.button(text="👤 Мой профиль")
    b.button(text="📊 Сдать отчет за неделю")
    b.button(text="💡 Совет дня")
    b.adjust(2)
    return b.as_markup(resize_keyboard=True)

def get_diet_kb():
    b = ReplyKeyboardBuilder()
    for t in ["Мясоед", "Вегетарианец", "Фастфуд-лайф"]: b.button(text=t)
    return b.adjust(1).as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(m: types.Message, state: FSMContext):
    await m.answer("🔥 Добро пожаловать в Elite Fitness \nВыбери свою цель на ближайшие 6 месяцев:", 
                   reply_markup=get_main_kb())
    await state.set_state(Registration.goal)

@dp.message(Registration.goal)
async def reg_goal(m: types.Message, state: FSMContext):
    await state.update_data(goal=m.text)
    await m.answer("Как мне тебя называть?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.name)

@dp.message(Registration.name)
async def reg_name(m: types.Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer(f"Приятно познакомиться, {m.text}! Сколько тебе лет?")
    await state.set_state(Registration.age)

@dp.message(Registration.age)
async def reg_age(m: types.Message, state: FSMContext):
    val = extract_number(m.text)
    if not val: return await m.answer("Напиши возраст числом!")
    await state.update_data(age=int(val))
    await m.answer("Твой текущий вес (кг)?")
    await state.set_state(Registration.weight)

@dp.message(Registration.weight)
async def reg_weight(m: types.Message, state: FSMContext):
    val = extract_number(m.text)
    if not val: return await m.answer("Напиши вес числом!")
    await state.update_data(weight=val)
    await m.answer("Твой рост (см)?")
    await state.set_state(Registration.height)

@dp.message(Registration.height)
async def reg_height(m: types.Message, state: FSMContext):
    val = extract_number(m.text)
    if not val: return await m.answer("Напиши рост числом!")
    await state.update_data(height=int(val))
    await m.answer("Сколько дней в неделю готов тренироваться?")
    await state.set_state(Registration.train_days)

@dp.message(Registration.train_days)
async def reg_days(m: types.Message, state: FSMContext):
    await state.update_data(train_days=m.text)
    await m.answer("Выбери тип питания:", reply_markup=get_diet_kb())
    await state.set_state(Registration.diet_type)

@dp.message(Registration.diet_type)
async def reg_diet(m: types.Message, state: FSMContext):
    await state.update_data(diet=m.text)
    await m.answer("И последнее: сколько часов в сутки ты обычно спишь?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Registration.sleep_hours)

@dp.message(Registration.sleep_hours)
async def final_reg(m: types.Message, state: FSMContext):
    sleep_val = extract_number(m.text)
    if not sleep_val: return await m.answer("Напиши количество часов числом!")
    
    data = await state.get_data()
    u_id = m.from_user.id
    
    w, h, a = data['weight'], data['height'], data['age']
    bmr = int(10 * w + 6.25 * h - 5 * a + 5)
    
    goal = data['goal']
    if "Похудение" in goal: 
        t_cal = bmr - 400
        pred = "📉 За 6 месяцев ты сможешь сбросить около **12-15 кг**."
    elif "Массонабор" in goal: 
        t_cal = bmr + 500
        pred = "📈 За 6 месяцев ты наберешь **10-12 кг** массы."
    elif "Эстета" in goal: 
        t_cal = bmr + 200
        pred = "🔱 За 6 месяцев ты создашь атлетичный рельеф и наберешь **5 кг** мышц."
    else: 
        t_cal = bmr
        pred = "⚖️ Ты сохранишь вес, но значительно улучшишь качество тела."

    db_save_user(u_id, data['name'], goal, w, h, a, t_cal, data['diet'])
    
    diet_info = DIETS.get(data['diet'], DIETS["Мясоед"])
    report = (
        f"🏆 **ПЕРСОНАЛЬНЫЙ ПЛАН ДЛЯ {data['name'].upper()}**\n\n"
        f"📅 **ТВОЯ ЦЕЛЬ НА 6 МЕСЯЦЕВ:**\n{pred}\n\n"
        f"📈 **Метаболизм:** База — {bmr} ккал.\n"
        f"🎯 **Целевое питание:** {t_cal} ккал.\n\n"
        f"🍎 **ПРИМЕР МЕНЮ:**\n"
        f"— Завтрак: {diet_info['Завтрак'][0]}\n"
        f"— Обед: {diet_info['Обед'][0]}\n"
        f"— Ужин: {diet_info['Ужин'][0]}\n\n"
        f"💪 **ТРЕНИРОВКИ:**\n"
    )
    for ex in WORKOUTS.get(goal, WORKOUTS["⚖️ Поддержание формы"]):
        report += f"• {ex}\n"
    
    report += "\n🚀 Каждое воскресенье жду от тебя отчет! Нажми кнопку в меню."
    
    await m.answer(report, parse_mode="Markdown", reply_markup=get_menu_kb())
    await state.clear()

@dp.message(F.text == "👤 Мой профиль")
async def cmd_profile(m: types.Message):
    p = db_get_profile(m.from_user.id)
    if not p: return await m.answer("Сначала пройди регистрацию! /start")
    
    text = (f"👤 ТВОЙ ПРОФИЛЬ:\n\n"
            f"Имя: {p[1]}\nЦель: {p[2]}\nВес: {p[3]} кг\nРост: {p[4]} см\n"
            f"Норма: {p[6]} ккал\nДиета: {p[7]}\n"
            f"Дата старта: {p[8]}")
    await m.answer(text, parse_mode="Markdown")

@dp.message(F.text == "📊 Сдать отчет за неделю")
async def report_start(m: types.Message, state: FSMContext):
    if not db_get_profile(m.from_user.id): return await m.answer("Заполни анкету! /start")
    await m.answer("📊 ОТЧЕТ ЗА НЕДЕЛЮ\nКакой у тебя вес сегодня (кг)?", 
                   reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(WeeklyReport.weight)

@dp.message(WeeklyReport.weight)
async def report_w(m: types.Message, state: FSMContext):
    val = extract_number(m.text)
    if not val: return await m.answer("Введи только число!")
    await state.update_data(w=val)
    await m.answer("Сколько тренировок ты провел за эти 7 дней?")
    await state.set_state(WeeklyReport.trains)

@dp.message(WeeklyReport.trains)
async def report_t(m: types.Message, state: FSMContext):
    val = extract_number(m.text)
    if not val: return await m.answer("Введи число!")
    await state.update_data(t=int(val))
    await m.answer("Оцени свою дисциплину в еде от 1 до 5 (где 5 — идеально):")
    await state.set_state(WeeklyReport.diet_score)

@dp.message(WeeklyReport.diet_score)
async def report_d(m: types.Message, state: FSMContext):
    val = extract_number(m.text)
    if not val or val > 5: return await m.answer("Введи число от 1 до 5!")
    await state.update_data(d=int(val))
    await m.answer("Сколько часов в среднем ты спал?")
    await state.set_state(WeeklyReport.sleep)

@dp.message(WeeklyReport.sleep)
async def report_final(m: types.Message, state: FSMContext):
    sleep_val = extract_number(m.text)
    data = await state.get_data()
    u_id = m.from_user.id
    
    new_w = data['w']
    old_w = db_get_last_weight(u_id)
    diff = round(new_w - old_w, 2)
    
    db_save_report(u_id, new_w, data['t'], data['d'], sleep_val)
    
    if diff < 0: result = f"✅ Круто! Ты скинул **{abs(diff)} кг**."
    elif diff > 0: result = f"📈 Вес увеличился на **{diff} кг**."
    else: result = "⚖️ Вес на месте. Стабильность — залог успеха!"
    
    feedback = "🔥 Отличная работа на этой неделе! Продолжаем!" if data['d'] >= 4 else "⚠️ На следующей неделе старайся меньше нарушать режим питания."
    
    await m.answer(f"📊 **ИТОГИ НЕДЕЛИ:**\n\n{result}\n\n"
                   f"Тренировок: {data['t']}\nСон: {sleep_val} ч.\n\n{feedback}", 
                   parse_mode="Markdown", reply_markup=get_menu_kb())
    await state.clear()

@dp.message(F.text == "💡 Совет дня")
async def cmd_tips(m: types.Message):
    import random
    tips = [
        "Пей минимум 2 литра воды в день для обмена веществ.",
        "Последний прием пищи должен быть за 2-3 часа до сна.",
        "Не забывай про растяжку после тренировки.",
        "Сон — лучшее время для роста мышц и жиросжигания.",
        "Белок — это строительный материал. Убедись, что его достаточно."
    ]
    await m.answer(f"💡 СОВЕТ:\n{random.choice(tips)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())