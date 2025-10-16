import cloudscraper
from bs4 import BeautifulSoup

def get_grades(iin, password):
    scraper = cloudscraper.create_scraper()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "ru,en;q=0.9",
    }

    # 1️⃣ Получаем токен из страницы логина
    login_page = scraper.get("https://college.snation.kz/kz/tko/login", headers=headers)
    soup = BeautifulSoup(login_page.text, "html.parser")
    token_tag = soup.find("meta", {"name": "csrf-token"})
    token = token_tag["content"] if token_tag else None

    if not token:
        return "⚠️ Не удалось получить токен авторизации."

    # 2️⃣ Авторизация
    payload = {
        "_token": token,
        "iin": iin,
        "password": password,
    }

    login_resp = scraper.post("https://college.snation.kz/kz/tko/login", data=payload, headers=headers)
    if "Қате" in login_resp.text or "error" in login_resp.text.lower():
        return "❌ Неверный ИИН немесе құпия сөз."

    # 3️⃣ Загружаем страницу журналов
    journals = scraper.get("https://college.snation.kz/ru/tko/control/journals", headers=headers)
    if journals.status_code != 200:
        return "⚠️ Не удалось открыть страницу журналов."

    # 4️⃣ Берем первую ссылку на журнал
    soup = BeautifulSoup(journals.text, "html.parser")
    first_journal = soup.find("a", href=lambda href: href and "/control/journals/" in href)
    if not first_journal:
        return "📄 Журнал не найден."

    journal_url = "https://college.snation.kz" + first_journal["href"]
    journal_resp = scraper.get(journal_url, headers=headers)

    # 5️⃣ Парсим оценки
    soup = BeautifulSoup(journal_resp.text, "html.parser")
    dates = [d.get_text(strip=True) for d in soup.select("tr.sc-journal__table--head-row div.sc-journal__table--cell-value")]
    grades = [g.get_text(strip=True) for g in soup.select("tr.sc-journal__table--row div.sc-journal__table--cell-value")]

    if not dates or not grades:
        return "📄 Оценки не найдены."

    result = "📘 *Сіздің бағаларыңыз:*\n\n"
    for date, grade in zip(dates, grades):
        result += f"📅 {date}: {grade or '—'}\n"

    return result
