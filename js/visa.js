const cards = ["46782346", "45781218", "79874568", "12157845", "36151845", "41250895", "41201961"];
let visaCount = 0;

// Перебираем все карты в массиве
for (let i = 0; i < cards.length; i++) {
    // Если номер карты начинается с цифры 4, увеличиваем счетчик
    if (cards[i].startsWith("4")) {
        visaCount++;
    }
}

// Выводим итоговое сообщение
console.log(`Карт VISA ${visaCount} из ${cards.length}.`);