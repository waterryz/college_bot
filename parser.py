from bs4 import BeautifulSoup

def get_grades_from_html(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Находим таблицу с оценками
    table = soup.find('table', class_='sc-journal__table--scroll-part')
    if not table:
        return "⚠️ Таблица оценок не найдена."

    # Извлекаем даты
    head_row = table.find('tr', class_='sc-journal__table--head-row')
    dates = [cell.get_text(strip=True) for cell in head_row.find_all('div', class_='sc-journal__table--cell-value')]

    # Извлекаем оценки (вторая строка)
    data_row = table.find('tr', class_='sc-journal__table--row')
    grades = [cell.get_text(strip=True) for cell in data_row.find_all('div', class_='sc-journal__table--cell-value')]

    # Формируем результат
    result = "📘 *Журнал оценок:*\n\n"
    for date, grade in zip(dates, grades):
        result += f"📅 {date}: {grade if grade else '—'}\n"

    return result
