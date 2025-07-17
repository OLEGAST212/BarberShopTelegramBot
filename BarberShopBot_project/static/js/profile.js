import { tg } from "./common.js";

document.addEventListener("DOMContentLoaded", async () => {
  tg.ready();

  const initData = Telegram.WebApp.initData;
  // 1) Сначала GET — подтягиваем существующий профиль
  let resp = await fetch(
    `/api/profile?init_data=${encodeURIComponent(initData)}`
  );
  if (!resp.ok) {
    console.error("Ошибка загрузки профиля:", resp.status);
    return;
  }
  let profile = await resp.json();

  // 2) Заполняем поля
  document.getElementById("first-name").value         = profile.first_name  || "";
  document.getElementById("last-name").value          = profile.last_name   || "";
  document.getElementById("profile-patronymic").value = profile.patronymic  || "";
  document.getElementById("phone").value              = profile.phone       || "";
  document.getElementById("email").value              = profile.email       || "";

  // 3) Кнопка «Назад»
  document.getElementById("profile-back").addEventListener("click", () => {
    window.location.href = "/";
  });

  // 4) Обработка сабмита
  document.getElementById("profile-form").addEventListener("submit", async e => {
    e.preventDefault();
    const payload = {
      init_data:  initData,
      first_name:  document.getElementById("first-name").value,
      last_name:   document.getElementById("last-name").value,
      patronymic:  document.getElementById("profile-patronymic").value,
      phone:       document.getElementById("phone").value,
      email:       document.getElementById("email").value,
    };

    resp = await fetch("/api/profile", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(payload),
    });
    if (!resp.ok) {
      console.error("Ошибка сохранения профиля:", resp.status);
      alert("Не удалось сохранить профиль");
      return;
    }
    // повторно получаем данные из ответа
    profile = await resp.json();

    // обновляем поля заново, на всякий случай
    document.getElementById("first-name").value         = profile.first_name;
    document.getElementById("last-name").value          = profile.last_name;
    document.getElementById("profile-patronymic").value = profile.patronymic;
    document.getElementById("phone").value              = profile.phone;
    document.getElementById("email").value              = profile.email;

    alert("✅ Профиль сохранён");
  });
});
