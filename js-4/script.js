let count = 0;
const counterDisplay = document.getElementById('counter-value');

function updateCounter() {
    counterDisplay.textContent = count;
    
    if (count > 0) {
        counterDisplay.style.color = 'green';
    } else if (count < 0) {
        counterDisplay.style.color = 'red';
    } else {
        counterDisplay.style.color = 'grey';
    }
}

document.getElementById('btn-decrease').addEventListener('click', function() {
    count--;
    updateCounter();
});

document.getElementById('btn-reset').addEventListener('click', function() {
    count = 0;
    updateCounter();
});

document.getElementById('btn-increase').addEventListener('click', function() {
    count++;
    updateCounter();
});

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

const lottoContainer = document.getElementById('lotto-container');

document.getElementById('btn-lotto').addEventListener('click', function() {
    lottoContainer.innerHTML = '';
    
    let numbers = [];
    
    while (numbers.length < 6) {
        let randomNum = getRandomInt(1, 99);
        if (!numbers.includes(randomNum)) {
            numbers.push(randomNum);
        }
    }

    for (let i = 0; i < numbers.length; i++) {
        let num = numbers[i];
        let displayNum = num < 10 ? '0' + num : num;
        
        let ball = document.createElement('div');
        ball.className = 'ball';
        ball.textContent = displayNum;
        
        lottoContainer.appendChild(ball);
    }
});