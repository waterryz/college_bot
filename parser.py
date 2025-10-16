import requests
from bs4 import BeautifulSoup

def get_grades(username: str, password: str):
    session = requests.Session()

    login_url = "https://college.snation.kz/login/index.php"
    journal_url = "https://college.snation.kz/grade/report/overview/index.php"

    # Авторизация
    payload = {
        "username": username,
        "password": password
    }
    response = session.post(login_url, data=payload)

    if "Неверный логин" in response.text or "Invalid" in response.text:
        return {"error": "Неверный логин или пароль"}

    # Переход к журналу
    journal_page = session.get(journal_url)
    soup = BeautifulSoup(journal_page.text, "html.parser")

    # Парсинг таблицы оценок
    grades = []
    table = soup.find("table", class_="generaltable")
    if not table:
        return {"error": "Не удалось найти таблицу с оценками"}

    for row in table.find_all("tr")[1:]:
        cols = [c.text.strip() for c in row.find_all("td")]
        if len(cols) >= 2:
            subject = cols[0]
            grade = cols[1]
            grades.append((subject, grade))

    if not grades:
        return {"error": "Оценок не найдено"}

    return {"grades": grades}

