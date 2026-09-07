// Запрашиваем число у пользователя и преобразуем в числовой тип
const multiplier = Number(prompt("Введите число от 2 до 10:"));

// Проверяем, входит ли число в заданный диапазон
if (multiplier >= 2 && multiplier <= 10) {
    // Запускаем цикл от 1 до 10
    for (let i = 1; i <= 10; i++) {
        console.log(`${multiplier} × ${i} =${multiplier * i}`);
    }
} else {
    console.log("Ошибка: нужно было ввести число от 2 до 10.");
}