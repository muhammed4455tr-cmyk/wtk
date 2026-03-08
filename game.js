const rooms = {
  giris: {
    name: "Eski Giriş",
    text: "Paslı kapı arkanızdan kilitlendi. Uzaktan zincir sesi geliyor.",
    choices: [
      { label: "Sola dön (Depo)", next: "depo" },
      { label: "İleri yürü (Koridor)", next: "koridor" },
    ],
  },
  depo: {
    name: "Tozlu Depo",
    text: "Rafların arasında bir el feneri var. Ama arkanda nefes sesi duyuluyor.",
    item: "Fener",
    choices: [
      { label: "Feneri al ve çık", next: "koridor" },
      { label: "Hiç oyalanmadan çık", next: "koridor", damage: 1, log: "Karanlıkta bir şeye çarptın." },
    ],
  },
  koridor: {
    name: "Uzun Koridor",
    text: "Duvarlarda çizikler var. İki kapı görüyorsun.",
    choices: [
      { label: "Sağ kapı (Ayna Odası)", next: "ayna" },
      { label: "Sol kapı (Çıkış Kapısı)", next: "cikis" },
    ],
  },
  ayna: {
    name: "Ayna Odası",
    text: "Aynadaki yansıman sana ait değil. Gölge saldırıyor.",
    choices: [
      { label: "Kaç!", next: "cikis", damage: 1, log: "Gölge omzunu yaraladı." },
    ],
  },
  cikis: {
    name: "Mühürlü Çıkış",
    text: "Kapının yanında kırmızı bir kilit var. Sadece ışıkla açılıyor gibi.",
    choices: [
      { label: "Kapıyı zorla", ending: "bad", damage: 2, log: "Kapı açılmadı, içerideki şey sana yetişti." },
      { label: "Fenerle kilidi aydınlat", ending: "good", requires: "Fener" },
    ],
  },
};

const state = {
  room: "giris",
  health: 3,
  inventory: [],
  gameOver: false,
};

const healthEl = document.getElementById("health");
const roomEl = document.getElementById("room-name");
const inventoryEl = document.getElementById("inventory");
const descriptionEl = document.getElementById("description");
const choicesEl = document.getElementById("choices");
const logEl = document.getElementById("log");
const restartButton = document.getElementById("restart");

function addLog(text) {
  const li = document.createElement("li");
  li.textContent = text;
  logEl.prepend(li);
}

function render() {
  const room = rooms[state.room];

  healthEl.textContent = String(state.health);
  roomEl.textContent = room.name;
  inventoryEl.textContent = state.inventory.length ? state.inventory.join(", ") : "Boş";
  descriptionEl.textContent = room.text;
  choicesEl.innerHTML = "";

  if (!state.gameOver && room.item && !state.inventory.includes(room.item)) {
    state.inventory.push(room.item);
    addLog(`${room.item} bulundu.`);
  }

  if (state.gameOver) {
    restartButton.hidden = false;
    return;
  }

  room.choices.forEach((choice) => {
    const button = document.createElement("button");
    button.textContent = choice.label;
    button.addEventListener("click", () => choose(choice));
    choicesEl.appendChild(button);
  });
}

function endGame(type) {
  state.gameOver = true;
  choicesEl.innerHTML = "";

  if (type === "good") {
    descriptionEl.textContent = "Kilidin işareti sönüyor. Kapı açıldı ve geceye kaçtın. Yaşıyorsun... şimdilik.";
    addLog("İyi son: Hayatta kaldın.");
  } else {
    descriptionEl.textContent = "Işıklar tamamen söndü. Ayak sesleri yaklaştı. Bu binadan çıkamadın.";
    addLog("Kötü son: Karanlık seni yuttu.");
  }

  render();
}

function choose(choice) {
  if (choice.requires && !state.inventory.includes(choice.requires)) {
    addLog(`Bu seçim için ${choice.requires} gerekiyor.`);
    return;
  }

  if (choice.damage) {
    state.health -= choice.damage;
    addLog(choice.log || "Hasar aldın.");
  }

  if (state.health <= 0) {
    endGame("bad");
    return;
  }

  if (choice.ending) {
    endGame(choice.ending);
    return;
  }

  state.room = choice.next;
  render();
}

restartButton.addEventListener("click", () => {
  state.room = "giris";
  state.health = 3;
  state.inventory = [];
  state.gameOver = false;
  logEl.innerHTML = "";
  restartButton.hidden = true;
  addLog("Oyun yeniden başladı.");
  render();
});

addLog("Kaçış başladı.");
render();
