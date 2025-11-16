import re

file_path = r"C:\Users\ASUS\Desktop\all in\IUCA\python\лаба 10\mockdata.txt"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

names = re.findall(r'^(\w+)', text, flags=re.MULTILINE)

surnames = re.findall(r'^\w+\s+(\w+)', text, flags=re.MULTILINE)

types = re.findall(r'\.(\w+)\b', text)

print("Имена:")
for n in names:
    print(n)

print("\nФамилии:")
for s in surnames:
    print(s)

print("\nТипы файлов:")
for t in types:
    print(t)