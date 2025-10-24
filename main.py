from decouple import config
import psycopg2
from src.api import HeadHunterAPI
from src.db import DBManager
from src.files import WorkingWithData


def create_database(password: str):
    """Создание базы данных vacancies_hh_ru."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=354354,
            host="localhost",
            port=5432,
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS vacancies_hh_ru;")
        conn.close()
    except psycopg2.Error as e:
        print(f"Ошибка создания БД: {e}")
        raise


def process_option(api, db, option):
    options = {
        "1": lambda: process_option_1(api),
        "2": lambda: process_option_2(api),
        "3": lambda: process_option_3(),
        "4": lambda: process_option_4(api, db),
        "5": lambda: process_option_5(db),
        "6": lambda: process_option_6(db),
        "7": lambda: process_option_7(db),
        "8": lambda: process_option_8(db),
        "9": lambda: process_option_9(api, db),
        "0": lambda: db.close() or exit(),
    }
    action = options.get(option, lambda: print("Неверный выбор"))
    action()


def process_option_1(api):
    """Поиск и сохранение вакансий в JSON."""
    kw = input("Введите ключевое слово для поиска вакансий: ")
    vacs = api.get_vacancies({"text": kw, "per_page": 100})
    file_handler = WorkingWithData(filepath="data/vacancies.json")
    for vac in vacs:
        file_handler.add_to_json(vac)
    print(f"Сохранено {len(vacs)} вакансий в data/vacancies.json")


def process_option_2(api):
    """Поиск и сохранение работодателя в JSON."""
    name = input("Введите название компании: ")
    emps = api.get_employers({"text": name, "per_page": 1})
    file_handler = WorkingWithData(filepath="data/employers.json")
    if emps:
        file_handler.add_to_json(emps[0])
        print(f"Сохранен работодатель {emps[0]['name']}")
    else:
        print("Работодатель не найден")


def process_option_3():
    """Просмотр сохраненных данных из JSON."""
    file_handler = WorkingWithData(filepath="data/vacancies.json")
    data = file_handler.read_json()
    if data:
        for item in data:
            print(f"Вакансия: {item.get('name')}, URL: {item.get('url')}")
    else:
        print("Нет сохраненных вакансий.")


def process_option_4(api, db):
    companies = [
        "Яндекс",
        "Газпром",
        "Сбербанк",
        "Ростелеком",
        "Лукойл",
        "Норникель",
        "Авито",
        "Ozon",
        "Mail.ru",
        "Тинькофф",
    ]
    for name in companies:
        emps = api.get_employers({"text": name, "per_page": 1})
        if emps:
            emp = emps[0]
            db.save_employer(emp)
            vacs = api.get_vacancies({"employer_id": emp["id"], "per_page": 100})
            for v in vacs:
                db.save_vacancy(v, emp["id"])
            print(f"Загружено: {emp['name']} + {len(vacs)} вакансий")


def process_option_5(db):
    for n, c in db.get_companies_and_vacancies_count():
        print(f"{n}: {c}")


def process_option_6(db):
    for row in db.get_all_vacancies():
        print(f"{row[0]} | {row[1]} | {row[2]}-{row[3]} {row[4]}")


def process_option_7(db):
    print(f"Средняя: {db.get_avg_salary():.0f}")


def process_option_8(db):
    for row in db.get_vacancies_with_higher_salary():
        print(f"{row[0]} | {row[1]} | {row[2]}-{row[3]}")


def process_option_9(api, db):
    kw = input("Слово: ")
    for row in db.get_vacancies_with_keyword(kw):
        print(f"{row[0]} | {row[1]}")


def main():
    password = config("DB_PASSWORD")
    create_database(password)
    api = HeadHunterAPI()
    db = DBManager(password)
    db.create_tables()

    while True:
        print("\n" + "=" * 50)
        print("1. Поиск вакансий (в JSON)")
        print("2. Поиск работодателей (в JSON)")
        print("3. Просмотр JSON")
        print("4. Загрузить компании в PostgreSQL")
        print("5. Компании и кол-во вакансий (БД)")
        print("6. Все вакансии (БД)")
        print("7. Средняя зарплата (БД)")
        print("8. Вакансии выше средней (БД)")
        print("9. Поиск по слову (БД)")
        print("0. Выход")
        choice = input("→ ")
        process_option(api, db, choice)


if __name__ == "__main__":
    main()
