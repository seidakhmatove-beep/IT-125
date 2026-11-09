const gameList = document.querySelector('#game-list');
const gameCount = document.querySelector('#game-count');
const loadError = document.querySelector('#load-error');
const dialog = document.querySelector('#game-dialog');
const editor = document.querySelector('#game-editor');
const gameForm = document.querySelector('#game-form');
const storageKey = 'logo-game-catalog';
let games = [];
let editingId = null;

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

  const actions = document.createElement('div');
  actions.className = 'game-card-actions';
  const edit = document.createElement('button');
  edit.className = 'game-details-button';
  edit.type = 'button';
  edit.textContent = 'Изменить';
  edit.addEventListener('click', () => openEditor(game));
  const remove = document.createElement('button');
  remove.className = 'game-details-button game-delete-button';
  remove.type = 'button';
  remove.textContent = 'Удалить';
  remove.addEventListener('click', () => deleteGame(game.id));

  actions.append(edit, remove);
  content.append(genre, title, description, details, actions);
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

function renderGames() {
  gameList.replaceChildren(...games.map(createGameCard));
  gameCount.textContent = `Игр в каталоге: ${games.length}`;
}

function saveGames() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(games));
    renderGames();
    return true;
  } catch {
    document.querySelector('#editor-error').textContent = 'Не удалось сохранить данные в браузере.';
    document.querySelector('#editor-error').hidden = false;
    return false;
  }
}

function openEditor(game = null) {
  editingId = game?.id ?? null;
  gameForm.reset();
  document.querySelector('#editor-error').hidden = true;
  document.querySelector('#editor-title').textContent = game ? 'Изменить игру' : 'Добавить игру';
  if (game) {
    gameForm.elements.title.value = game.title;
    gameForm.elements.genre.value = game.genre;
    gameForm.elements.image.value = game.image;
    gameForm.elements.description.value = game.description;
    gameForm.elements.platforms.value = game.platforms.join(', ');
  }
  editor.showModal();
}

function deleteGame(id) {
  if (!window.confirm('Удалить эту игру из каталога?')) return;
  const previousGames = games;
  games = games.filter((game) => game.id !== id);
  if (!saveGames()) games = previousGames;
}

gameForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(gameForm);
  const game = {
    id: editingId ?? Math.max(0, ...games.map((item) => Number(item.id) || 0)) + 1,
    title: formData.get('title').trim(),
    genre: formData.get('genre').trim(),
    image: formData.get('image').trim(),
    description: formData.get('description').trim(),
    platforms: formData.get('platforms').split(',').map((platform) => platform.trim()).filter(Boolean)
  };
  const previousGames = games;
  games = editingId === null
    ? [...games, game]
    : games.map((item) => item.id === editingId ? game : item);
  if (saveGames()) editor.close();
  else games = previousGames;
});

fetch('js/games.json')
  .then((response) => {
    if (!response.ok) throw new Error('Не удалось получить JSON');
    return response.json();
  })
  .then((originalGames) => {
    try {
      const savedGames = localStorage.getItem(storageKey);
      games = savedGames === null ? originalGames : JSON.parse(savedGames);
      if (!Array.isArray(games)) throw new Error('Некорректный каталог');
      renderGames();
    } catch {
      games = originalGames;
      renderGames();
      loadError.hidden = false;
      loadError.textContent = 'Не удалось прочитать сохранённый каталог. Очистите данные сайта в браузере.';
    }
  })
  .catch(() => {
    gameCount.textContent = 'Каталог недоступен';
    loadError.hidden = false;
  });

document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
document.querySelector('#add-game').addEventListener('click', () => openEditor());
document.querySelector('#editor-close').addEventListener('click', () => editor.close());
document.querySelector('#editor-cancel').addEventListener('click', () => editor.close());
dialog.addEventListener('click', (event) => {
  if (event.target === dialog) dialog.close();
});
editor.addEventListener('click', (event) => {
  if (event.target === editor) editor.close();
});
