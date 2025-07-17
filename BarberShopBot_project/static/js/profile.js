// js/profile.js
document.addEventListener("DOMContentLoaded", async () => {
  const tg = window.Telegram.WebApp;
  tg.ready();

  // 1) достаём init_data
  const params   = new URLSearchParams(window.location.search);
  const initData = params.get("init_data") || Telegram.WebApp.initData || "";
  if (!initData) return alert("Ошибка: нет init_data");

  // 2) GET профиль из API
  const resp = await fetch(`/api/profile?init_data=${encodeURIComponent(initData)}`);
  if (!resp.ok) return alert("Не удалось загрузить профиль");
  const profile = await resp.json();

  // 3) заполняем форму
  document.getElementById("first-name").value         = profile.first_name;
  document.getElementById("last-name").value          = profile.last_name;
  document.getElementById("profile-patronymic").value = profile.patronymic;
  document.getElementById("phone").value              = profile.phone;
  document.getElementById("email").value              = profile.email;

  // 4) Назад
  document.getElementById("profile-back").addEventListener("click", () => {
    location.href = `index.html?init_data=${encodeURIComponent(initData)}`;
  });

  // 5) Сохранение
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
    const r2 = await fetch("/api/profile", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(payload)
    });
    if (!r2.ok) return alert("Ошибка сохранения");
    alert("✅ Профиль сохранён");
  });
});
