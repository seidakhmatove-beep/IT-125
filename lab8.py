class Account:
    def __init__(self, account_number, balance, pin_code):
        self.__account_number = account_number
        self.__balance = balance
        self.__pin_code = pin_code
    def deposit(self, amount, pin):
        if pin == self.__pin_code:
            self.__balance += amount
    def withdraw(self, amount, pin):
        if pin == self.__pin_code and amount <= self.__balance:
            self.__balance -= amount
    def get_balance(self, pin):
        if pin == self.__pin_code:
            return self.__balance

acc = Account('123456789012', 4000, 1234)
pin = input('Введите pin: ')
try:
    pin_int = int(pin)
except:
    pin_int = pin
if pin == '1234' or pin_int == 1234:
    print(acc.get_balance(pin_int))
else:
    print('Ошибка')


class Product:
    def __init__(self, name, price):
        self.name = name
        self.__price = price
    def set_discount(self, percent):
        if percent < 0:
            print("Процент скидки не может быть отрицательным.")
        else:
            new_price = self.__price * (1 - percent / 100)
            if new_price < 0:
                self.__price = 0
            else:
                self.__price = new_price
    def final_price(self):
        return self.__price

my_product = Product('Лук', 25)
my_product.set_discount(10)
print(my_product.final_price())


class Course:
    def __init__(self, name, students, max_places):
        self.__name = name
        self.__students = students
        self.__max_places = max_places
    def add_student(self, name):
        if len(self.__students) < self.__max_places:
            self.__students.append(name)
            print(f'{name} был/а добавлен/а в список.')
        else:
            print('Нет мест.')
    def remove_student(self, name):
        if name in self.__students:
            self.__students.remove(name)
            print(f'{name} был/а удален/а из списка.')
        else:
            print('Не найден/а в списке.')
    def get_students(self):
        return self.__students.copy()

my_course = Course('OOP', [], 2)
my_course.add_student('Аня')
my_course.add_student('Венера')
my_course.add_student('Артем')
print(my_course.get_students())
my_course.remove_student('Венера')
print(my_course.get_students())


class SmartWatch:
    def __init__(self, battery):
        self.__battery = battery
    def use(self, minutes):
        decrease = minutes / 10
        self.__battery -= decrease
        if self.__battery < 0:
            self.__battery = 0
        print(f'Заряд: {self.__battery}')
    def charge(self, percent):
        self.__battery += percent
        if self.__battery > 100:
            self.__battery = 100
        print(f'Заряд: {self.__battery}')
    def get_battery(self):
        return self.__battery

my_watch = SmartWatch(56)
my_watch.use(20)
print(my_watch.get_battery())
my_watch.charge(15)
print(my_watch.get_battery())


class Transport:
    def __init__(self, speed, capacity):
        self.speed = speed
        self.capacity = capacity
    def travel_time(self, distance):
        return distance / self.speed

class Bus(Transport):
    pass
class Train(Transport):
    pass
class Airplane(Transport):
    def travel_time(self, distance):
        time = super().travel_time(distance)
        return time * 0.8

bus = Bus(90, 45)
train = Train(125, 125)
airplane = Airplane(600, 200)
distance = 1800
print(bus.travel_time(distance))
print(train.travel_time(distance))
print(airplane.travel_time(distance))


class Order:
    def __init__(self, food, base_price):
        self.food = food
        self.base_price = base_price
    def calculate_total(self):
        return self.base_price

class DineInOrder(Order):
    def calculate_total(self):
        tip = self.base_price * 0.1
        return self.base_price + tip

class TakeAwayOrder(Order):
    def calculate_total(self):
        discount = self.base_price * 0.05
        return self.base_price - discount

class DeliveryOrder(Order):
    def calculate_total(self):
        delivery = self.base_price * 0.15
        return self.base_price + delivery

order = Order('Манты', 250)
dine_in_order = DineInOrder('Манты', 250)
print(dine_in_order.calculate_total())
take_away_order = TakeAwayOrder('Манты', 250)
print(take_away_order.calculate_total())
delivery_order = DeliveryOrder('Манты', 250)
print(delivery_order.calculate_total())


class Character:
    def __init__(self, name, HP, ATK):
        self.name = name
        self.hp = HP
        self.atk = ATK
    def attack(self):
        pass
    def __str__(self):
        return f'{self.name} HP:{self.hp}'

class Warrior(Character):
    def attack(self):
        print(f"{self.name} атакует касой.")
class Mage(Character):
    def attack(self):
        print(f"{self.name} атакует магией.")
class Archer(Character):
    def attack(self):
        print(f"{self.name} атакует с ружьем.")

warrior = Warrior('Элфа', 2400, 90)
mage = Mage('Ава', 2400, 100)
archer = Archer('Рома', 2300, 90)
warrior.attack()
mage.attack()
archer.attack()
print(warrior)
print(mage)
print(archer)


class MediaFile:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration
    def play(self):
        pass

class AudioFile(MediaFile):
    def play(self):
        print(f'Воспроизводится аудио: {self.title} {self.duration} минут.')
class VideoFile(MediaFile):
    def play(self):
        print(f'Воспроизводится видео: {self.title} {self.duration} минут.')
class Podcast(MediaFile):
    def play(self):
        print(f'Воспроизводится эпизод: {self.title} {self.duration} минут.')

a = AudioFile("Песня Мияги", 3)
b = VideoFile("Клип Мияги", 5)
c = Podcast("Интервью Мияги", 40)
a.play()
b.play()
c.play()


from abc import ABC, abstractmethod
class PaymentSystem(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardPayment(PaymentSystem):
    def process_payment(self, amount):
        print(f'Оплата в сумму {amount} кредитной картой прошла успешно.')
class CryptoPayment(PaymentSystem):
    def process_payment(self, amount):
        print(f'Оплата в сумму {amount} По QR прошла успешно.')
class BankTransfer(PaymentSystem):
    def process_payment(self, amount):
        print(f'Оплата в сумму {amount} банковским переводом прошла успешно.')

card = CreditCardPayment()
crypto = CryptoPayment()
bank = BankTransfer()
card.process_payment(4000)
crypto.process_payment(200)
bank.process_payment(20000)


from abc import ABC, abstractmethod
class Animal(ABC):
    @abstractmethod
    def eat(self):
        pass
    def sleep(self):
        pass

class Lion(Animal):
    def eat(self):
        print('Лев ест зебру.')
    def sleep(self):
        print('Лев спит.')
class Elephant(Animal):
    def eat(self):
        print('Обезьяна питается бананами.')
    def sleep(self):
        print('Обезьяна спит взабрашися на дерево.')
class Snake(Animal):
    def eat(self):
        print('Змея питается маленькими животными.')
    def sleep(self):
        print('Змея спит свернувшись клубком.')

lion = Lion()
elephant = Elephant()
snake = Snake()
lion.eat(); lion.sleep()
elephant.eat(); elephant.sleep()
snake.eat(); snake.sleep()


from abc import ABC, abstractmethod
class Document(ABC):
    @abstractmethod
    def open(self):
        pass
    def edit(self):
        pass
    def save(self):
        pass

class WordDocument(Document):
    def open(self): print('Открыт документ Word.')
    def edit(self): print('Редактируется документ Word.')
    def save(self): print('Файл сохранён.')
class PdfDocument(Document):
    def open(self): print('Открыт PDF документ.')
    def edit(self): print('Редактируется PDF документ.')
    def save(self): print('Файл сохранён.')
class SpreadsheetDocument(Document):
    def open(self): print('Открыта таблица.')
    def edit(self): print('Редактируется таблица.')
    def save(self): print('Файл сохранён.')

word = WordDocument()
pdf = PdfDocument()
sheet = SpreadsheetDocument()
word.open(); word.edit(); word.save()
pdf.open(); pdf.edit(); pdf.save()
sheet.open(); sheet.edit(); sheet.save()


class EmailNotification:
    def send(self, message):
        print(f'Отправка Email: {message}')
class SMSNotification:
    def send(self, message):
        print(f'Отправка SMS: {message}')
class PushNotification:
    def send(self, message):
        print(f'Отправка Push-уведомления: {message}')

notifications = [EmailNotification(), SMSNotification(), PushNotification()]
for notification in notifications:
    notification.send("Привет!")


class Square:
    def __init__(self, side):
        self.side = side
    def perimeter(self):
        print(4 * self.side)

class Circle:
    def __init__(self, radius):
        self.radius = radius
    def perimeter(self):
        print(2 * 3.14 * self.radius)

class Triangle:
    def __init__(self, side1, side2, side3):
        self.a = side1
        self.b = side2
        self.c = side3
    def perimeter(self):
        print(self.a + self.b + self.c)

shapes = [Square(4), Circle(3), Triangle(2, 4, 6)]
for shape in shapes:
    shape.perimeter()


class Manager:
    def work(self):
        print('Бухгалтер управляет отчетами.')
class Developer:
    def work(self):
        print('Тестировщик проверяет и тестирует.')
class Designer:
    def work(self):
        print('Дизайнер. Создаёт дизайн интерфейсов.')
employees = [Manager(), Developer(), Designer()]
for employee in employees:
    employee.work()


class FireSpell:
    def cast(self, target):
        print(f"{target} получает урон от меча")
class IceSpell:
    def cast(self, target):
        print(f"{target} Заморожен!")
class HealingSpell:
    def cast(self, target):
        print(f"{target} восстанавливает здоровье!")