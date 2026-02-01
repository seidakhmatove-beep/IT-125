
from data import QUESTIONS

class QuizGame:
    def __init__(self, user_id):
        self.user_id = user_id
        self.current_question_index = 0
        self.correct_answers = 0
        self.wrong_answers = 0

        self.questions = QUESTIONS

    def get_current_question(self):
        """Возвращает текущий вопрос или None, если вопросы кончились"""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def check_answer(self, selected_index):
        """Проверяет ответ и обновляет счетчики"""
        current_q = self.get_current_question()
        if current_q:
            if int(selected_index) == current_q['correct_index']:
                self.correct_answers += 1
                return True
            else:
                self.wrong_answers += 1
                return False
        return False

    def next_question(self):
        """Переходит к следующему вопросу"""
        self.current_question_index += 1

    def is_finished(self):
        """Проверяет, закончилась ли викторина"""
        return self.current_question_index >= len(self.questions)

    def get_results(self):
        """Формирует текст с результатами"""
        total = len(self.questions)
        percentage = (self.correct_answers / total) * 100
        text = (
            f"🏁 **Викторина завершена!**\n\n"
            f"✅ Правильных ответов: {self.correct_answers}\n"
            f"❌ Ошибок: {self.wrong_answers}\n"
            f"📊 Твой результат: {percentage:.1f}%"
        )
        return text