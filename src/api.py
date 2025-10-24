from abc import ABC, abstractmethod
import requests


class BaseHeadHunterAPI(ABC):
    """
    Абстрактный класс для HeadHunterAPI.
    """

    @abstractmethod
    def get_vacancies(self, params=None):
        """Получение вакансий с API."""
        pass

    @abstractmethod
    def get_employers(self, params=None):
        """Получение работодателей с API."""
        pass


class HeadHunterAPI(BaseHeadHunterAPI):
    """
    Класс, наследующийся от абстрактного класса, для работы с платформой hh.ru.
    """

    def __init__(self):
        self.base_url = "https://api.hh.ru"
        self.vacancies_url = f"{self.base_url}/vacancies"
        self.employers_url = f"{self.base_url}/employers"

    def get_vacancies(self, params=None):
        """
        Получение вакансий с API hh.ru.
        """
        try:
            response = requests.get(self.vacancies_url, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к API: {e}")
            return []

    def get_employers(self, params=None):
        """
        Получение работодателей с API hh.ru.
        """
        try:
            response = requests.get(self.employers_url, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к API: {e}")
            return []
