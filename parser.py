import cloudscraper
from bs4 import BeautifulSoup

def get_grades(login, password):
    scraper = cloudscraper.create_scraper()

    # 1. Получаем страницу логина и CSRF-токен
    login_url = "https://college.snation.kz/kz/tko/login"
    login_page = scraper.get(login_url)
    soup = BeautifulSoup(login_page.text, "html.parser")
    csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]

    # 2. Авторизация
    payload = {
        "iin": login,
        "password": password,
        "remember": "false",
        "type": "iin"
    }
    headers = {
        "X-CSRF-TOKEN": csrf_token,
        "Referer": login_url
    }

    resp = scraper.post(login_url, data=payload, headers=headers, cookies=login_page.cookies)

    # 3. Проверка успешности
    try:
        data = resp.json()
        if not data.get("success", False):
            return "❌ Неверный ИИН либо пароль."
    except:
        if "Қате" in resp.text or "error" in resp.text.lower():
            return "❌ Неверный ИИН либо пароль."

    # 4. Загружаем журнал
    journal_url = "https://college.snation.kz/ru/tko/control/journals"
    response = scraper.get(journal_url)
    if response.status_code != 200:
        return "⚠️ Не удалось открыть страницу журнала."

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="sc-journal__table--scroll-part")
    if not table:
        return "📄 Оценки не найдены."

    # 5. Парсим таблицу
    dates = [th.get_text(strip=True) for th in table.select("tr.sc-journal__table--head-row div.sc-journal__table--cell-value")]
    grades = [td.get_text(strip=True) for td in table.select("tr.sc-journal__table--row div.sc-journal__table--cell-value")]

    result = "📘 *Сіздің журнал:* \n\n"
    for date, grade in zip(dates, grades):
        result += f"📅 {date}: {grade or '—'}\n"

    return result
