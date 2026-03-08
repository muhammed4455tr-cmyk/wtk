# Ofisten Kaçış (MVP Prototip)

Bu repo, istediğin konsept için **kurulabilir bir başlangıç prototipi** içerir:
- Ofis içinde kaçış senaryosu
- Silahla düşman vurma
- Araba anahtarı bulma
- Araca gidip debriyaj + kontak ile çalıştırma sekansı
- Türkçe arayüz/metinler

> Not: Bu sürüm hızlı bir MVP'dir. Gerçekçi AAA seviye animasyon/ses ve tam çevrim içi altyapı için ek geliştirme gerekir.

## Kurulum (Windows)

1. Python 3.11+ kur.
2. `setup\\install_windows.bat` dosyasını çalıştır.
3. Oyun otomatik başlar.

## Manuel kurulum

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python src/main.py
```

## Kontroller

- `WASD`: Hareket
- `Mouse Sol Tık`: Ateş
- `E`: Etkileşim (anahtar alma / arabaya geçme)
- `CTRL`: Debriyaj (araba çalıştırma sekansında basılı tut)
- `I`: Kontak (debriyaja basılıyken)

## Online demo (temel)

Ayrı bir temel ağ demosu eklidir:

Sunucu:
```bash
python src/server.py
```

İstemci (oyuncu):
```bash
python src/online_demo.py --name oyuncu1 --host SUNUCU_IP
```

Bu demo, farklı ağlarda oynamak için port yönlendirme/NAT ayarı gerektirebilir.
