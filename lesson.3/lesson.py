flags = {
    'ru': {'red blue', 'white'},
    'kg': {"red yellow", 'red'},
    'ua': {"red blue", 'red', 'blue'},
    'uk': {"yellow", "blue"},
    'fr': {'white', 'blue', 'red'},
    'ch': {"white", "red", "blue"},
    'bg': {"white", "graide", "red"},
}


while True:
     colors = input("Введите цвета через пробел (или 'exit' для выхода): ").lower()
     if colors == "exit":
         print("Программа завершена.")
         break
     
     colors = set(colors.split())
     result = []
     
     
     for country, flag_colors in flags.items():
         if colors.issubset(flag_colors):
             result.append('domain')
             
     if result:
        print("Домены с такими цветами:'red', 'blue", 'white' .join(result))
            
     else:
        print("Нет флагов с такими цветами.")