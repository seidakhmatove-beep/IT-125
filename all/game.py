import random

class Game:
    def __init__(self, lives=3, bullets=2, total_chambers=6):
        self.max_lives = lives
        self.lives = lives
        self.bullets = bullets
        self.total_chambers = total_chambers
        self.reset_round()

    def reset_round(self):
        self.bullet_positions = random.sample(range(1, self.total_chambers + 1), self.bullets)
        self.current_position = 1
        self.alive = True

    def full_reset(self):
        self.lives = self.max_lives
        self.reset_round()

    def shot(self):
        if not self.alive or self.lives <= 0:
            return "game over"
        
        if self.current_position in self.bullet_positions:
            self.lives -= 1
            self.alive = False
            return "boom"
        else:
            self.current_position += 1
            return "empty"