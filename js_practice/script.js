function sumArrays(arr1, arr2) {
    if (arr1.length === 0) {
        return arr2;
    }
    if (arr2.length === 0) {
        return arr1;
    }

    var result = []; 
    for (var i = 0; i < arr1.length; i++) {
        result.push(arr1[i] + arr2[i]);
    }
    return result;
}

console.log('Тест 1:', sumArrays([1, 2, 3], [5, 10, 12])); // [6, 12, 15]
console.log('Тест 2:', sumArrays([1, 2, 3], []));           // [1, 2, 3]

let book1 = { title: "Алиса в Стране чудес", author: "Льюис Кэрролл", year: 1865 };
let book2 = { title: "Анна Каренина", author: "Лев Толстой", year: 1878 };
let book3 = { title: "Автостопом по Галактике", author: "Дуглас Адамс", year: 2016 };

let booksList = [book1, book2, book3];
console.log('Задание 2 (Список книг):', booksList);

var headerElement = document.createElement('header');
headerElement.textContent = 'Header';
document.body.appendChild(headerElement);

var mainElement = document.createElement('main');
var sectionElement = document.createElement('section');

var divContainer = document.createElement('div');
divContainer.className = 'container';

var heading = document.createElement('h2');
heading.className = 'text-2xl';
heading.textContent = 'Секция 1';

var paragraph = document.createElement('p');
paragraph.className = 'text-gray text-sm';
paragraph.textContent = 'Lorem ipsum dolor sit amet, consectetur.';

divContainer.appendChild(heading);
divContainer.appendChild(paragraph);
sectionElement.appendChild(divContainer);
mainElement.appendChild(sectionElement);
document.body.appendChild(mainElement);

var footerElement = document.createElement('footer');
footerElement.textContent = 'Footer';
document.body.appendChild(footerElement);


var select = document.querySelector('select');
var redBtns = document.getElementsByClassName('btn-red');
var greenBtns = document.getElementsByClassName('btn-green');

function checkButtons() {
    if (select.value === 'Зеленые кнопки') {
        for (var i = 0; i < greenBtns.length; i++) {
            greenBtns[i].style.display = 'inline-block';
        }
        for (var j = 0; j < redBtns.length; j++) {
            redBtns[j].style.display = 'none';
        }
    } else if (select.value === 'Красные кнопки') {
        for (var i = 0; i < redBtns.length; i++) {
            redBtns[i].style.display = 'inline-block';
        }
        for (var j = 0; j < greenBtns.length; j++) {
            greenBtns[j].style.display = 'none';
        }
    }
}

select.addEventListener('change', checkButtons);

checkButtons();