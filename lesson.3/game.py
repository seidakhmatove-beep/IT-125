import random

def main():
    print("=" * 50)
    print("ПОБЕГ ИЗ Темницы")
    print("=" * 50)
    print("Вы просыпаетесь в холодном каменном подземелье.")
    print("Голова раскалывается, и вы ничего не помните.")
    print("Ваша цель — найти выход и выжить!")
    print("-" * 50)
    
    play_again = True
    
    while play_again:
        inventory = []
        
        print("\nПеред вами две двери: левая и правая.")
        choice1 = input("Какую выберете? (левая/правая): ").lower()
        
        if choice1 == "левая":
            print("\nВы входите в комнату с старым деревянным сундуком.")
            choice2 = input("Открыть его? (да/нет): ").lower()
            
            if choice2 == "да":
                print("Внутри вы нашли ржавый ключ! Вы взяли его с собой.")
                inventory.append("ключ")
            else:
                print("Вы решили не рисковать и прошли мимо.")
                
            print("Вы выходите в длинный темный коридор.")
            
        elif choice1 == "правая":
            print("\nВы сделали несколько шагов и пол провалился под ногами!")
            print("Вы падаете в глубокую яму...")
            print("ИГРА ОКОНЧЕНА")
            
            again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
            if again != "да":
                play_again = False
            continue
        else:
            print("Не понимаю ваш выбор. Попробуйте еще раз.")
            continue
        
        print("\nВ конце коридора вы видите дверь, а рядом спит стражник.")
        
        if "ключ" in inventory:
            print("Вы используете ключ и тихо открываете дверь.")
            door_unlocked = True
        else:
            print("У вас нет ключа. Придется попытаться прокрасться мимо стражника.")
            luck = random.choice([True, False])
            
            if luck:
                print("Вам повезло! Вы успешно проскользнули мимо.")
                door_unlocked = True
            else:
                print("Стражник проснулся и схватил вас!")
                print("ИГРА ОКОНЧЕНА")
                
                again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
                if again != "да":
                    play_again = False
                continue
        
        if door_unlocked:
            print("\nВы в комнате с дверью, защищенной кодовым замком.")
            print("У вас есть 3 попытки чтобы угадать код (3 цифры).")
            
            secret_code = random.randint(100, 999)
            attempts = 3
            
            while attempts > 0:
                try:
                    guess = int(input(f"Попытка {4-attempts}/3. Введите код: "))
                    
                    if guess == secret_code:
                        print("Щелк! Замок открылся!")
                        break
                    else:
                        attempts -= 1
                        if attempts > 0:
                            print(f"Неверно! Осталось попыток: {attempts}")
                        else:
                            print("Замочек щелкнул в последний раз и навсегда заблокировался.")
                            print("ИГРА ОКОНЧЕНА")
                            
                            again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
                            if again != "да":
                                play_again = False
                            break
                except ValueError:
                    print("Пожалуйста, введите число!")
            
            if attempts == 0:
                continue
                
            print("\nЗа дверью вы видите две лестницы.")
            choice3 = input("Куда пдете? (вверх/вниз): ").lower()
            
            if choice3 == "вверх":
                print("\nВы поднимаетесь по лестнице и видите свет!")
                print("Свежий воздух ударяет в лицо - вы на свободе!")
                print("ПОЗДРАВЛЯЮ! ВЫ ПОБЕДИЛИ!")
                
            elif choice3 == "вниз":
                print("\nВы спускаетесь в темную пещеру с странными светящимися грибами.")
                choice4 = input("Попробовать один? (да/нет): ").lower()
                
                if choice4 == "да":
                    print("Гриб оказался ядовитым... Вам становится плохо.")
                    print("ИГРА ОКОНЧЕНА")
                else:
                    print("Вы wisely решили не есть незнакомые грибы.")
                    print("Придется вернуться к развилке.")
                    choice3 = input("Куда пойдете? (вверх/вниз): ").lower()
                    if choice3 == "вверх":
                        print("\nВы поднимаетесь по лестнице и видите свет!")
                        print("Свежий воздух ударяет в лицо - вы на свободе!")
                        print("ПОЗДРАВЛЯЮ! ВЫ ПОБЕДИЛИ!")
                    else:
                        print("Вы снова спустились вниз и заблудились в темноте...")
                        print("ИГРА ОКОНЧЕНА")
            else:
                print("Не понимаю ваш выбор.и вас находит стража.")
                print("ИГРА ОКОНЧЕНА")
        
        again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
        if again != "да":
            play_again = False
    
    print("\nСпасибо за игру! До свидания!")
