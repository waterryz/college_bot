import requests
from bs4 import BeautifulSoup

def get_grades(login, password):
    session = requests.Session()

    # Авторизация через ЖСН (ИИН)
    login_url = "https://college.snation.kz/kz/tko/login"
    payload = {
        "iin": login,
        "password": password,
        "remember": "false"
    }

    resp = session.post(login_url, data=payload)
    if resp.status_code != 200:
        return "⚠️ Сервер недоступен."

    if "Қате" in resp.text or "error" in resp.text.lower():
        return "❌ Неверное имя пользователя или пароль."

    # Получаем журнал
    journal_url = "https://college.snation.kz/ru/tko/control/journals"
    response = session.get(journal_url)

    if response.status_code != 200:
        return "⚠️ Не удалось открыть страницу журнала."

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="sc-journal__table--scroll-part")

    if not table:
        return "📄 Оценки не найдены."

    # Парсим таблицу
    dates = [th.get_text(strip=True) for th in table.select("tr.sc-journal__table--head-row div.sc-journal__table--cell-value")]
    grades = [td.get_text(strip=True) for td in table.select("tr.sc-journal__table--row div.sc-journal__table--cell-value")]

    result = "📘 *Сіздің журнал:* \n\n"
    for date, grade in zip(dates, grades):
        result += f"📅 {date}: {grade or '—'}\n"

    return result
