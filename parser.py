import re
import cloudscraper
from bs4 import BeautifulSoup

def get_grades(login, password):
    scraper = cloudscraper.create_scraper()  # Обходит Cloudflare
    login_page = "https://college.snation.kz/kz/tko/login"

    # 1️⃣ Получаем страницу входа, чтобы достать CSRF-токен
    try:
        resp = scraper.get(login_page)
    except Exception:
        return "⚠️ Серверге қосылу мүмкін емес / Не удалось подключиться к серверу."

    if resp.status_code != 200:
        return "⚠️ Сервер жауап бермейді / Сервер не отвечает."

    match = re.search(r'name="csrf-token" content="([^"]+)"', resp.text)
    if not match:
        return "⚠️ Қате: CSRF-токен табылмады / Ошибка: не найден CSRF-токен."
    csrf = match.group(1)

    headers = {
        "X-CSRF-TOKEN": csrf,
        "Referer": login_page,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    payload = {
        "iin": login,
        "password": password,
        "remember": "false"
    }

    # 2️⃣ Отправляем запрос на авторизацию
    resp = scraper.post(login_page, data=payload, headers=headers)
    if resp.status_code != 200:
        return "⚠️ Кіру қатесі / Ошибка входа."

    # Если ответ содержит слова "қате" — значит, неправильный пароль
    if "қате" in resp.text.lower() or "error" in resp.text.lower():
        return "❌ ИИН немесе құпия сөз қате / Неверный ИИН или пароль."

    # 3️⃣ Переходим к журналу
    journal_url = "https://college.snation.kz/ru/tko/control/journals"
    response = scraper.get(journal_url, headers=headers)

    if response.status_code != 200:
        return "⚠️ Журналды ашу мүмкін емес / Не удалось открыть страницу журнала."

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    if not table:
        return "📄 Бағалар табылмады / Оценки не найдены."

    # 4️⃣ Парсим таблицу
    rows = table.find_all("tr")
    result = "📘 *Сіздің журнал:* / *Ваш журнал:* \n\n"

    for row in rows[1:]:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if cols:
            result += f"📚 {cols[0]} — {cols[-1]}\n"

    return result or "⚠️ Журнал бос / Журнал пуст."
