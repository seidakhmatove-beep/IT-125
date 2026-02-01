
import telebot
from telebot import types
import config
from quiz import QuizGame

bot = telebot.TeleBot(config.TOKEN)


games = {}


@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.chat.id

    games[user_id] = QuizGame(user_id)

    bot.send_message(user_id, "Привет! Начинаем викторину по Python из 15 вопросов. Поехали!")
    send_question(user_id)


def send_question(user_id):

    game = games.get(user_id)

    if not game or game.is_finished():

        if game:
            bot.send_message(user_id, game.get_results(), parse_mode='Markdown')
            del games[user_id]
        return

    question_data = game.get_current_question()


    markup = types.InlineKeyboardMarkup()
    for idx, option in enumerate(question_data['options']):

        button = types.InlineKeyboardButton(text=option, callback_data=str(idx))
        markup.add(button)


    try:
        bot.send_photo(
            user_id,
            question_data['img_url'],
            caption=f"❓ Вопрос {game.current_question_index + 1}/15:\n\n**{question_data['text']}**",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        bot.send_message(user_id, f"Ошибка загрузки картинки. Вопрос: {question_data['text']}", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    user_id = call.message.chat.id
    game = games.get(user_id)

    if not game:
        bot.answer_callback_query(call.id, "Игра не найдена. Напишите /start")
        return


    selected_index = int(call.data)


    is_correct = game.check_answer(selected_index)


    if is_correct:
        bot.answer_callback_query(call.id, "✅ Верно!")
    else:
        bot.answer_callback_query(call.id, "❌ Ошибка!")


    bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)


    game.next_question()
    send_question(user_id)


if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()