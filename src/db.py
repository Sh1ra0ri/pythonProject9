import psycopg2
from typing import List, Tuple, Dict, Any, cast


class DBManager:
    """Модуль для взаимодействия с PostgreSQL."""
    def __init__(self, password: str):
        self.conn = psycopg2.connect(
            dbname="vacancies_hh_ru",
            user="postgres",
            password=password,
            host="localhost",
            port=5432,
        )

    def create_tables(self):
        """Создание таблиц employers и vacancies."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    DROP TABLE IF EXISTS vacancies;
                    DROP TABLE IF EXISTS employers;

                    CREATE TABLE employers (
                        employer_id INTEGER PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        url TEXT
                    );

                    CREATE TABLE vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        title VARCHAR(255) NOT NULL,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        currency VARCHAR(10),
                        url VARCHAR(255),
                        description TEXT,
                        city VARCHAR(100)
                    );
                """
                )
                self.conn.commit()
        except psycopg2.Error as e:
            print(f"Ошибка создания таблиц: {e}")
            raise

    def save_employer(self, employer: Dict[str, Any]):
        """Сохранение данных о работодателе."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO employers (employer_id, name, url)
                VALUES (%s, %s, %s) ON CONFLICT (employer_id) DO NOTHING;
                """,
                (employer["id"], employer["name"], employer.get("alternate_url")),
            )
            self.conn.commit()

    def save_vacancy(self, vacancy: Dict[str, Any], employer_id: int):
        """Сохранение данных о вакансии."""
        salary_from = vacancy.get("salary", {}).get("from")
        salary_to = vacancy.get("salary", {}).get("to")
        currency = vacancy.get("salary", {}).get("currency")
        description = vacancy.get("description", "")
        city = vacancy.get("area", {}).get("name", "")

        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO vacancies (employer_id, title, salary_from, salary_to, currency, url, description, city)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    employer_id,
                    vacancy.get("name", ""),
                    salary_from,
                    salary_to,
                    currency,
                    vacancy.get("alternate_url", ""),
                    description,
                    city,
                ),
            )
            self.conn.commit()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получение списка компаний и количества вакансий."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, COUNT(v.vacancy_id)
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name ORDER BY COUNT DESC;
                """
            )
            result = cur.fetchall()
            return cast(List[Tuple[str, int]], result)

    def get_all_vacancies(self) -> List[Tuple]:
        """Получение списка всех вакансий."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.currency, v.url
                FROM vacancies v JOIN employers e ON v.employer_id = e.employer_id;
                """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Получение средней зарплаты."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((COALESCE(salary_from, salary_to) + COALESCE(salary_to, salary_from)) / 2)
                FROM vacancies WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
                """
            )
            res = cur.fetchone()[0]
            return round(res, 2) if res else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Получение вакансий с зарплатой выше средней."""
        avg = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v JOIN employers e ON v.employer_id = e.employer_id
                WHERE COALESCE(v.salary_from, v.salary_to) > %s;
                """,
                (avg,),
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Получение вакансий по ключевому слову."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v JOIN employers e ON v.employer_id = e.employer_id
                WHERE LOWER(v.title) LIKE LOWER(%s);
                """,
                (f"%{keyword}%",),
            )
            return cur.fetchall()

    def close(self):
        self.conn.close()
