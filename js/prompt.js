const inputColor = prompt("Введите цвет светофора:");

if (inputColor) {
    const color = inputColor.trim().toLowerCase();

    switch (color) {
        case "красный":
            console.log("Красный : стой!");
            break;
        case "желтый":
        case "жёлтый":
            console.log("Желтый : жди!");
            break;
        case "зеленый":
        case "зелёный":
            console.log("Зеленый : иди!");
            break;
        default:
            console.log("Такого цвета у светофора нет");
    }
} else {
    console.log("Цвет не введен");
}

// Запросил цвет через prompt перевел введенную строку в нижний регистр с помощью .toLowerCase, чтобы программа работала вне зависимости от регистра (например, если введут «Красный» с большой буквы)
//  Выбор сделал через конструкцию switch и case — так код выглядит понятнее, чем куча ветвей if.