
const fioRegex = /^[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?\s+[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?\s+[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?$/;
const phoneRegex = /^\+996\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{3}$/;
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function checkField(input, regex, errorMessage) {
  input.addEventListener('input', function () {
    const value = this.value.trim();
    this.setCustomValidity(value && !regex.test(value) ? errorMessage : '');
  });
}

document.querySelectorAll('[data-fio]').forEach(input =>
  checkField(input, fioRegex, 'Введите ФИО полностью: Фамилия Имя Отчество.')
);
document.querySelectorAll('[data-phone]').forEach(input =>
  checkField(input, phoneRegex, 'Введите номер в формате +996 555 123 456.')
);
document.querySelectorAll('[data-email]').forEach(input =>
  checkField(input, emailRegex, 'Введите правильный адрес почты.')
);

const supportForm = document.getElementById('support-form');
if (supportForm) {
  supportForm.addEventListener('submit', event => {
    event.preventDefault();
    if (!supportForm.checkValidity()) {
      supportForm.reportValidity();
      return;
    }
    document.getElementById('support-note').textContent =
      'Спасибо! Форма заполнена. Отправка обращений появится после подключения сервера.';
    supportForm.reset();
  });
}
