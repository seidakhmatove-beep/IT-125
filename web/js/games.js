const gameList = document.querySelector('#game-list');
const gameCount = document.querySelector('#game-count');
const loadError = document.querySelector('#load-error');
const dialog = document.querySelector('#game-dialog');

function createGameCard(game) {
  const card = document.createElement('article');
  card.className = 'game-card';

  const image = document.createElement('img');
  image.src = game.image;
  image.alt = game.title;
  image.loading = 'lazy';

  const content = document.createElement('div');
  const genre = document.createElement('small');
  genre.textContent = game.genre;
  const title = document.createElement('h3');
  title.textContent = game.title;
  const description = document.createElement('p');
  description.textContent = game.description;
  const details = document.createElement('button');
  details.className = 'game-details-button';
  details.type = 'button';
  details.textContent = 'Подробнее →';
  details.addEventListener('click', () => showGameDetails(game));

  content.append(genre, title, description, details);
  card.append(image, content);
  return card;
}

function showGameDetails(game) {
  document.querySelector('#detail-image').src = game.image;
  document.querySelector('#detail-image').alt = game.title;
  document.querySelector('#detail-genre').textContent = game.genre;
  document.querySelector('#detail-title').textContent = game.title;
  document.querySelector('#detail-description').textContent = game.description;
  document.querySelector('#detail-platforms').textContent = game.platforms.join(', ');
  dialog.showModal();
}

fetch('js/games.json')
  .then((response) => {
    if (!response.ok) throw new Error('Не удалось получить JSON');
    return response.json();
  })
  .then((games) => {
    gameList.replaceChildren(...games.map(createGameCard));
    gameCount.textContent = `Игр в каталоге: ${games.length}`;
  })
  .catch(() => {
    gameCount.textContent = 'Каталог недоступен';
    loadError.hidden = false;
  });

document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (event) => {
  if (event.target === dialog) dialog.close();
});
