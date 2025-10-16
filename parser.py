import cloudscraper
from bs4 import BeautifulSoup

def get_grades(login: str, password: str) -> str:
    # создаем сессию через cloudscraper (обходит Cloudflare)
    session = cloudscraper.create_scraper()

    # --- Авторизация ---
    login_url = "https://college.snation.kz/kz/tko/login"
    payload = {
        "iin": login,
        "password": password,
        "remember": "false"
    }

    try:
        resp = session.post(login_url, data=payload, timeout=15)
    except Exception as e:
        return f"⚠️ Сервер недоступен.\n🔧 Подробности: {e}"

    # проверяем ответ
    if resp.status_code != 200:
        return "⚠️ Сервер недоступен."

    if any(x in resp.text for x in ["Қате", "error", "invalid", "қате енгізілді"]):
        return "❌ Неверный ЖСН или пароль.\n⚠️ Тексеру: ЖСН немесе құпия сөз қате."

    # --- Получаем список журналов ---
    journal_root = "https://college.snation.kz/ru/tko/control/journals"
    response = session.get(journal_root)

    if response.status_code != 200:
        return "⚠️ Не удалось открыть страницу журналов.\n⚠️ Журнал парағы ашылмады."

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)
    journal_links = [f"https://college.snation.kz{a['href']}" for a in links if "/tko/control/journals/" in a["href"]]

    if not journal_links:
        return "📄 Журналы табылмады. Оценки не найдены."

    result = "📘 *Твоё расписание / Сенің бағаларың:*\n\n"

    # --- Парсим каждый журнал ---
    for link in journal_links:
        journal_page = session.get(link)
        soup = BeautifulSoup(journal_page.text, "html.parser")

        subject = soup.find("h1")
        subject_name = subject.get_text(strip=True) if subject else "Без названия"

        table = soup.find("table", class_="sc-journal__table--scroll-part")
        if not table:
            result += f"📗 {subject_name}: Нет данных.\n"
            continue

        dates = [th.get_text(strip=True) for th in table.select("tr.sc-journal__table--head-row div.sc-journal__table--cell-value")]
        grades = [td.get_text(strip=True) for td in table.select("tr.sc-journal__table--row div.sc-journal__table--cell-value")]

        if not dates or not grades:
            result += f"📗 {subject_name}: пусто.\n"
            continue

        # Добавляем в результат
        result += f"📘 *{subject_name}*\n"
        for date, grade in zip(dates, grades):
            result += f"📅 {date}: {grade or '—'}\n"
        result += "\n"

    return result.strip()
