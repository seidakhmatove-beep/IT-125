(() => {
  const FAVORITES_KEY = 'freemarket-favorites';
  const PRODUCTS_KEY = 'freemarket-favorite-products';
  const ADS_KEY = 'freemarket-my-ads';
  const PROFILE_KEY = 'freemarket-profile';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  function readList(key) {
    try {
      const value = JSON.parse(localStorage.getItem(key) || '[]');
      return Array.isArray(value) ? value : [];
    } catch {
      return [];
    }
  }

  function writeData(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  function updateFavoriteButton(button) {
    const active = readList(FAVORITES_KEY).includes(button.dataset.favorite);
    button.classList.toggle('is-favorite', active);
    button.setAttribute('aria-pressed', String(active));
    button.textContent = active ? '♥' : '♡';
  }

  function toggleFavorite(button) {
    const favorites = readList(FAVORITES_KEY);
    const id = button.dataset.favorite;
    if (!favorites.includes(id)) {
      const card = button.closest('.product-card');
      const title = $('.product-title', card);
      const price = $('.product-price', card);
      const image = $('img', card);
      const meta = $('.product-meta', card);
      if (card && title && price && image) {
        let products = {};
        try { products = JSON.parse(localStorage.getItem(PRODUCTS_KEY) || '{}'); }
        catch { products = {}; }
        products[id] = {
          title: title.textContent.trim(),
          price: price.textContent.trim(),
          image: image.getAttribute('src'),
          imageAlt: image.getAttribute('alt') || title.textContent.trim(),
          meta: meta ? meta.textContent.trim() : '',
          href: title.getAttribute('href') || 'item.html'
        };
        localStorage.setItem(PRODUCTS_KEY, JSON.stringify(products));
      }
    }
    const nextFavorites = favorites.includes(id)
      ? favorites.filter((favoriteId) => favoriteId !== id)
      : [...favorites, id];
    writeData(FAVORITES_KEY, nextFavorites);
    updateFavoriteButton(button);
    document.dispatchEvent(new Event('favorites:changed'));
  }

  $$('[data-favorite]').forEach((button) => {
    updateFavoriteButton(button);
    button.addEventListener('click', () => toggleFavorite(button));
  });

  const favoritesContainer = $('[data-favorites-list]');
  if (favoritesContainer) {
    const sourceCards = $$('[data-product-id]');
    function renderFavorites() {
      const savedIds = readList(FAVORITES_KEY);
      let products = {};
      try { products = JSON.parse(localStorage.getItem(PRODUCTS_KEY) || '{}'); }
      catch { products = {}; }
      const visibleIds = savedIds.filter((id) =>
        sourceCards.some((card) => card.dataset.productId === id) || products[id]
      );
      favoritesContainer.replaceChildren();

      if (visibleIds.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'panel empty-state';
        const title = document.createElement('h2');
        title.textContent = 'Пока здесь пусто';
        const message = document.createElement('p');
        message.textContent = 'Нажмите на сердечко у объявления, чтобы сохранить его.';
        const link = document.createElement('a');
        link.className = 'button';
        link.href = 'catalog.html';
        link.textContent = 'Перейти в каталог';
        empty.append(title, message, link);
        favoritesContainer.append(empty);
        return;
      }

      visibleIds.forEach((id) => {
        const source = sourceCards.find((item) => item.dataset.productId === id);
        let card;
        if (source) {
          card = source.cloneNode(true);
        } else if (products[id]) {
          const product = products[id];
          card = document.createElement('article');
          card.className = 'product-card';
          const link = document.createElement('a');
          link.href = product.href;
          const image = document.createElement('img');
          image.className = 'product-image';
          image.src = product.image;
          image.alt = product.imageAlt;
          link.append(image);
          const body = document.createElement('div');
          body.className = 'product-body';
          const title = document.createElement('a');
          title.className = 'product-title';
          title.href = product.href;
          title.textContent = product.title;
          const price = document.createElement('div');
          price.className = 'product-price';
          price.textContent = product.price;
          body.append(title, price);
          if (product.meta) {
            const meta = document.createElement('div');
            meta.className = 'product-meta';
            meta.textContent = product.meta;
            body.append(meta);
          }
          card.append(link, body);
        } else {
          return;
        }

        let button = $('[data-favorite]', card);
        if (!button) {
          button = document.createElement('button');
          button.className = 'favorite-button';
          button.type = 'button';
          button.dataset.favorite = id;
          card.append(button);
        }
        button.classList.add('is-favorite');
        button.setAttribute('aria-label', 'Удалить из избранного');
        button.setAttribute('aria-pressed', 'true');
        button.textContent = '♥';
        button.addEventListener('click', () => toggleFavorite(button));
        favoritesContainer.append(card);
      });
    }
    renderFavorites();
    document.addEventListener('favorites:changed', renderFavorites);
  }

  $$('[data-show-phone]').forEach((button) => {
    button.addEventListener('click', () => {
      button.textContent = button.dataset.showPhone;
      button.disabled = true;
      button.setAttribute('aria-label', `Телефон продавца: ${button.dataset.showPhone}`);
    });
  });

  const navigation = $('[data-main-nav]');
  const menuButton = $('[data-menu-toggle]');
  if (navigation && menuButton) {
    menuButton.addEventListener('click', () => {
      const isOpen = navigation.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(isOpen));
    });
  }

  $$('[data-accordion-button]').forEach((button) => {
    button.addEventListener('click', () => {
      const answer = document.getElementById(button.getAttribute('aria-controls'));
      const wasOpen = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!wasOpen));
      if (answer) answer.hidden = wasOpen;
    });
  });

  const catalogSearch = $('[data-catalog-search]');
  const catalogCards = $$('[data-catalog-card]');
  function applyCatalogSearch(query) {
    const normalizedQuery = query.trim().toLocaleLowerCase('ru');
    catalogCards.forEach((card) => {
      const title = ($('.product-title', card)?.textContent || '').toLocaleLowerCase('ru');
      card.classList.toggle('search-hidden', !title.includes(normalizedQuery));
    });
  }

  if (catalogSearch) {
    const initialQuery = new URLSearchParams(window.location.search).get('q') || '';
    catalogSearch.value = initialQuery;
    applyCatalogSearch(initialQuery);
    catalogSearch.addEventListener('input', () => applyCatalogSearch(catalogSearch.value));
  }

  $$('[data-filter-form]').forEach((form) => {
    form.addEventListener('input', () => {
      const values = new FormData(form);
      const minPrice = Number(values.get('min-price') || 0);
      const maxPrice = Number(values.get('max-price') || Infinity);
      const minYear = Number(values.get('min-year') || 0);
      const maxMileage = Number(values.get('max-mileage') || Infinity);
      const selectedCity = values.get('city');
      const selectedCondition = values.get('condition');

      catalogCards.forEach((card) => {
        const price = Number(card.dataset.price || 0);
        const year = Number(card.dataset.year || 0);
        const mileage = Number(card.dataset.mileage || 0);
        const failsFilter = price < minPrice || price > maxPrice ||
          (selectedCity && selectedCity !== card.dataset.city) ||
          (selectedCondition && selectedCondition !== card.dataset.condition) ||
          (minYear && year < minYear) ||
          (maxMileage !== Infinity && mileage > maxMileage);
        card.classList.toggle('filter-hidden', Boolean(failsFilter));
      });
    });
  });

  const adForm = $('[data-ad-form]');
  if (adForm) {
    adForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const formData = new FormData(adForm);
      const ad = {
        id: Date.now(),
        title: String(formData.get('title') || '').trim(),
        category: String(formData.get('category') || ''),
        price: Number(formData.get('price')),
        description: String(formData.get('description') || '').trim(),
        city: String(formData.get('city') || ''),
        phone: String(formData.get('phone') || '').trim(),
        createdAt: new Date().toLocaleDateString('ru-RU')
      };
      const status = $('[data-form-status]', adForm);

      if (!ad.title || !ad.category || !ad.description || !ad.city || !ad.phone || !Number.isFinite(ad.price) || ad.price < 0) {
        if (status) status.textContent = 'Проверьте, что все обязательные поля заполнены корректно.';
        return;
      }

      const ads = readList(ADS_KEY);
      ads.push(ad);
      writeData(ADS_KEY, ads);
      if (status) status.textContent = 'Объявление сохранено в этом браузере. Откройте кабинет, чтобы увидеть его.';
      adForm.reset();
    });
  }

  const myAdsContainer = $('[data-my-ads]');
  if (myAdsContainer) {
    const myAds = readList(ADS_KEY);
    myAdsContainer.replaceChildren();
    if (myAds.length === 0) {
      const message = document.createElement('p');
      message.className = 'form-note';
      message.textContent = 'У вас пока нет добавленных объявлений.';
      myAdsContainer.append(message);
    } else {
      myAds.forEach((ad) => {
        const card = document.createElement('article');
        card.className = 'panel my-ad-card';
        const title = document.createElement('h3');
        title.textContent = ad.title;
        const price = document.createElement('p');
        price.className = 'product-price';
        price.textContent = `${ad.price.toLocaleString('ru-RU')} сом`;
        const details = document.createElement('p');
        details.className = 'form-note';
        details.textContent = `${ad.category} · ${ad.city} · ${ad.createdAt}`;
        const description = document.createElement('p');
        description.textContent = ad.description;
        card.append(title, price, details, description);
        myAdsContainer.append(card);
      });
    }
  }

  const profileForm = $('[data-profile-form]');
  if (profileForm) {
    const profile = (() => {
      try { return JSON.parse(localStorage.getItem(PROFILE_KEY) || 'null'); }
      catch { return null; }
    })();
    if (profile) {
      ['name', 'phone', 'city'].forEach((field) => {
        const input = $(`[name="${field}"]`, profileForm);
        if (input && profile[field]) input.value = profile[field];
      });
    }
    profileForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const data = new FormData(profileForm);
      const nextProfile = {
        name: String(data.get('name') || '').trim(),
        phone: String(data.get('phone') || '').trim(),
        city: String(data.get('city') || '')
      };
      localStorage.setItem(PROFILE_KEY, JSON.stringify(nextProfile));
      const status = $('[data-form-status]', profileForm);
      if (status) status.textContent = 'Настройки сохранены в этом браузере.';
    });
  }

  const contactForm = $('[data-contact-form]');
  if (contactForm) {
    contactForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const status = $('[data-form-status]', contactForm);
      if (status) status.textContent = 'Спасибо! Форма демонстрационная и не отправляет данные на сервер.';
      contactForm.reset();
    });
  }
})();
