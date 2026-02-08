import random
import time


class RouletteGame:
    def __init__(self, player1="Нурдин", player2="Сэф"):
        self.players = [player1, player2]
        self.current_player_index = 0
        self.bullets = [False] * 6
        self.bullets[random.randint(0, 5)] = True
        self.current_step = 0
        self.start_time = time.time()
        self.time_limit = 5
        self.is_game_over = False

    def get_current_player(self):
        return self.players[self.current_player_index]

    def reset_timer(self):
        self.start_time = time.time()

    def pull_trigger(self):
        """Возвращает результат выстрела: 'win', 'lose' или 'timeout'"""
        now = time.time()


        if now - self.start_time > self.time_limit:
            self.is_game_over = True
            return "timeout"


        if self.bullets[self.current_step]:
            self.is_game_over = True
            return "lose"


        self.current_step += 1

        self.current_player_index = 1 if self.current_player_index == 0 else 0
        self.reset_timer()
        return "survived"

    def get_status_message(self, result):
        player = self.get_current_player()
        if result == "timeout":
            return f"Время вышло! {player} слишком долго думал и проиграл!"
        if result == "lose":
            return f" БАХ! {player} проиграл! Игра окончена."
        if result == "survived":
            return f" Щелчок... {player} выжил. Теперь очередь следующего игрока!\nУ тебя есть 5 секунд!"