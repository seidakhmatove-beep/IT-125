const users = [
    {
        login: "admin",
        password: "123",
        name: "Эльдар (Админ)"
    },
    {
        login: "student",
        password: "555",
        name: "Имран"
    },
    {
        login: "qwerty",
        password: "111",
        name: "Нурсултан"
    },
    {
        login: "user_test",
        password: "test",
        name: "Алим"
    },
    {
        login: "boss",
        password: "777",
        name: "Хаким"
    }
];

const form = document.getElementById('authForm');
const messageDiv = document.getElementById('message');

form.addEventListener('submit', function(event) {
    event.preventDefault(); 

    const inputLogin = document.getElementById('login').value;
    const inputPassword = document.getElementById('password').value;

    const foundUser = users.find(user => user.login === inputLogin && user.password === inputPassword);

    if (foundUser) {
        messageDiv.textContent = `Привет, ${foundUser.name}! Вы успешно авторизовались.`;
        messageDiv.className = 'success';
    } else {
        messageDiv.textContent = 'Ошибка: Неверный логин или пароль.';
        messageDiv.className = 'error';
    }
});

function sumAll(...args) {
    let sum = 0;
    for (let i = 0; i < args.length; i++) {
        sum += args[i];
    }
    return sum;
}

console.log("sumAll(2,5,6,7) ->", sumAll(2, 5, 6, 7));
console.log("sumAll(1,2,3,4,5,6,7,8,9,10) ->", sumAll(1, 2, 3, 4, 5, 6, 7, 8, 9, 10));

const calcBtn = document.getElementById('calcBtn');
const numbersInput = document.getElementById('numbersInput');
const sumResultDiv = document.getElementById('sumResult');

calcBtn.addEventListener('click', function() {
    const value = numbersInput.value;
    if (!value.trim()) return;

    const numbersArray = value.split(',').map(item => Number(item.trim())).filter(item => !isNaN(item));
    const result = sumAll(...numbersArray);

    sumResultDiv.innerHTML = `<div class="sum-output">Сумма: <b>${result}</b></div>`;
});