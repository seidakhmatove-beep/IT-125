import re

# Регулярные выражения
name_regex = r"^[A-Za-z]+"
surname_regex = r"(?<=\t)[A-Za-z]+(?=\t)"
filetype_regex = r"\.\w{2,5}$"

# Файлы вывода
name_file = open("name.txt", "w", encoding="utf-8")
surname_file = open("surname.txt", "w", encoding="utf-8")
type_file = open("typeFile.txt", "w", encoding="utf-8")

# Читаем mockdata.txt
with open("mockdata.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split("\t")
        # parts[0] = Имя
        # parts[1] = Фамилия
        # parts[3] = Название файла

        name = re.search(name_regex, parts[0]).group()
        surname = parts[1]

        file = parts[3]
        file_type = re.search(filetype_regex, file).group()

        # Запись в файлы
        name_file.write(name + "\n")
        surname_file.write(surname + "\n")
        type_file.write(file_type + "\n")

name_file.close()
surname_file.close()
type_file.close()


