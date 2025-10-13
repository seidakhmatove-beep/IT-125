
class Animal:
    def __init__(self, name, age, habitat):
        self.name = name          
        self.age = age            
        self.habitat = habitat    

    def eat(self):
        print(f"{self.name} ест.")

    def sleep(self):
        print(f"{self.name} спит.")

    def info(self):
        print(f"Животное: {self.name}, Возраст: {self.age}, Среда обитания: {self.habitat}")


class Mammal(Animal):
    def __init__(self, name, age, habitat, fur_color):
        super().__init__(name, age, habitat)
        self.fur_color = fur_color  

    def feed_babies(self):
        print(f"{self.name} кормит детёнышей молоком.")

    def info(self):
        super().info()
        print(f"Тип: Млекопитающее, Цвет шерсти: {self.fur_color}")



class Reptile(Animal):
    def __init__(self, name, age, habitat, is_venomous):
        super().__init__(name, age, habitat)
        self.is_venomous = is_venomous  

    def crawl(self):
        print(f"{self.name} ползёт по земле.")

    def info(self):
        super().info()
        print(f"Тип: Пресмыкающееся, Ядовитое: {'Да' if self.is_venomous else 'Нет'}")


lion = Mammal("Лев", 5, "Саванна", "золотистая")
snake = Reptile("Кобра", 2, "Джунгли", True)

print("=== Информация о животных ===")
lion.info()
lion.eat()
lion.feed_babies()

print("\n")
snake.info()
snake.crawl()
snake.sleep()
