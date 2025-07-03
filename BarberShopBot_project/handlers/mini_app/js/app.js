// Ждём, пока внутри Web App Telegram загрузится
window.Telegram.WebApp.ready();

// Простая навигация внутри страницы
const servicesBtn = document.getElementById("services-btn");
const servicesList = document.getElementById("services-list");
const backBtn = document.getElementById("back-btn");

// Открыть список услуг
servicesBtn.addEventListener("click", () => {
  servicesList.classList.remove("hidden");
});

// Вернуться назад
backBtn.addEventListener("click", () => {
  servicesList.classList.add("hidden");
});

// Обработчики топ-меню и услуг
document.querySelectorAll("button[data-action]").forEach(btn => {
  btn.addEventListener("click", () => {
    const action = btn.dataset.action;
    switch(action) {
      case "address":
        alert("Наш адрес: г. Новосибирск, ул. Ленина, 10");
        break;
      case "appointments":
        alert("У вас нет записей.");
        break;
      case "share":
        window.Telegram.WebApp.shareData(JSON.stringify({url: window.location.href}));
        break;
      case "profile":
        alert("Профиль:\nИмя: Иван\nТелефон: +7...");
        break;
      case "wallet":
        alert("Баланс: 0 ₽");
        break;
      case "shop":
        window.open("https://shop.example.com", "_blank");
        break;
      case "reviews":
        alert("Отзывы:\n– Отлично стригут!");
        break;
      case "about":
        alert("Сибирь Барбершоп — лучшие мастера в городе.");
        break;
      case "lang":
        alert("Язык: Русский");
        break;
    }
  });
});
