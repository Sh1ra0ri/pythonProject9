from typing import Optional, Dict, Any


class Vacancy:
    """
    Класс для работы с вакансиями.
    """

    def __init__(self, vac: Dict[str, Any]):
        self.name = vac.get("name", "")
        self.url = vac.get("url", "")
        self.salary = self._get_salary(vac.get("salary"))
        self.employer_id = vac.get("employer", {}).get("id")
        self.employer_name = vac.get("employer", {}).get("name", "")

    def _get_salary(self, salary_data: Optional[Dict[str, Any]]) -> int:
        """
        Получение зарплаты из данных вакансии.
        """
        if not salary_data:
            return 0

        salary_from = salary_data.get("from")
        salary_to = salary_data.get("to")

        if salary_from:
            return salary_from
        elif salary_to:
            return salary_to
        else:
            return 0

    def to_dict(self) -> Dict[str, Any]:
        """
        Метод для преобразования объекта в словарь для записи в JSON.
        """
        return {
            "name": self.name,
            "url": self.url,
            "salary": self.salary,
            "employer_id": self.employer_id,
            "employer_name": self.employer_name,
        }

    @staticmethod
    def validate_salary(salary: Optional[int]) -> str:
        """
        Валидация зарплаты.
        """
        if salary is None or salary <= 0:
            return "Зарплата не указана"
        return str(salary)

    def __lt__(self, other) -> bool:
        """
        Сравнение вакансий по зарплате (меньше).
        """
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        return NotImplemented

    def __gt__(self, other) -> bool:
        """
        Сравнение вакансий по зарплате (больше).
        """
        if isinstance(other, Vacancy):
            return self.salary > other.salary
        return NotImplemented

    def __repr__(self) -> str:
        """
        Строковое представление объекта.
        """
        return f"Vacancy(name='{self.name}', url='{self.url}', salary='{self.salary}')"


class Employer:
    """
    Класс для работы с работодателями.
    """

    def __init__(self, emp: Dict[str, Any]):
        self.id = emp.get("id")
        self.name = emp.get("name", "")
        self.url = emp.get("url", "")
        self.description = emp.get("description", "")

    def to_dict(self) -> Dict[str, Any]:
        """
        Метод для преобразования объекта в словарь для записи в JSON.
        """
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "description": self.description,
        }

    def __repr__(self) -> str:
        """
        Строковое представление объекта.
        """
        return f"Employer(id='{self.id}', name='{self.name}')"
