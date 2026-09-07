const input = parseInt(prompt("Введите число от 1 до 9:"));

const romanNumbers = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX"
};

if (romanNumbers[input]) {
    console.log(`${input} -> ${romanNumbers[input]}`);
} else {
    console.log("Ошибка: нужно ввести число от 1 до 9!");
}

// Вместо кучи условий создал объект-словарь romanNumbers, где ключами служат цифры 1–9, а значениями — их римские записи
// Программа принимает число и сразу вытаскивает нужное значение по ключу romanNumbers input
//  Если число вне диапазона, сработает ветка else.