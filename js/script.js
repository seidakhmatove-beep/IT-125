const num1 = Number(prompt("Введите первое число:"));
const num2 = Number(prompt("Введите второе число:"));

if (isNaN(num1) || isNaN(num2)) {
    console.log("Ошибка: введено не число!");
} else if (num1 > num2) {
    console.log(`Число ${num1} больше, чем ${num2}`);
} else if (num2 > num1) {
    console.log(`Число ${num2} больше, чем ${num1}`);
} else {
    console.log("Числа равны");
}

// Так как prompt всегда возвращает текст я обернул его в Number чтобы перевести данные в числа
//  Затем через if  else if сравнил их и вывел результат в консоль
//  Также добавил проверку isNaN если пользователь случайно введет буквы