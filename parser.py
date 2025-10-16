import cloudscraper
from bs4 import BeautifulSoup

def get_grades(login, password):
    scraper = cloudscraper.create_scraper()
    
    # Получаем токен
    login_page = scraper.get("https://college.snation.kz/kz/tko/login")
    soup = BeautifulSoup(login_page.text, "html.parser")
    csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]

    headers = {"X-CSRF-TOKEN": csrf_token}
    payload = {
        "iin": login,
        "password": password,
        "remember": "false"
    }

    # Авторизация
    resp = scraper.post("https://college.snation.kz/kz/tko/login", data=payload, headers=headers)
    if resp.status_code != 200:
        return "⚠️ Сервер недоступен."

    if "Қате" in resp.text or "error" in resp.text.lower():
        return "❌ Неверный ИИН либо пароль."

    # Переходим в журнал
    journal_url = "https://college.snation.kz/ru/tko/control/journals"
    response = scraper.get(journal_url)

    if response.status_code != 200:
        return "⚠️ Не удалось открыть страницу журнала."

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="sc-journal__table--scroll-part")
    if not table:
        return "📄 Оценки не найдены."

    # Парсим оценки
    dates = [th.get_text(strip=True) for th in table.select("tr.sc-journal__table--head-row div.sc-journal__table--cell-value")]
    grades = [td.get_text(strip=True) for td in table.select("tr.sc-journal__table--row div.sc-journal__table--cell-value")]

    result = "📘 *Твой журнал:* \n\n"
    for date, grade in zip(dates, grades):
        result += f"📅 {date}: {grade or '—'}\n"

    return result
