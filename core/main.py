import telebot
from telebot import types
import config
from game_logic import RouletteGame

bot = telebot.TeleBot(config.TOKEN)
games = {}


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.chat.id
    games[user_id] = RouletteGame("Нурдин", "Сэф")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔫 Сделать выстрел!", callback_data="shoot"))

    bot.send_message(
        user_id,
        f"Игра началась!\nИгроки: {games[user_id].players[0]} и {games[user_id].players[1]}\n\n"
        f"Первым стреляет: {games[user_id].get_current_player()}\n"
        f"⏳ У вас всего 5 секунд на выстрел!",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_shoot(call):
    user_id = call.message.chat.id
    game = games.get(user_id)

    if not game or game.is_game_over:
        bot.answer_callback_query(call.id, "Начните новую игру командой /start")
        return

    result = game.pull_trigger()
    msg_text = game.get_status_message(result)

    if result == "survived":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(" Сделать выстрел!", callback_data="shoot"))

        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=msg_text,
            reply_markup=markup
        )
    else:
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message_id,
            text=msg_text
        )
        del games[user_id]


if __name__ == '__main__':
    bot.polling(none_stop=True)