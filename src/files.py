import json
from abc import ABC, abstractmethod


class BaseData(ABC):
    """
    Абстрактный класс для класса WorkingWithData.
    """

    @abstractmethod
    def read_json(self):
        """Чтение данных из JSON файла."""
        pass

    @abstractmethod
    def add_to_json(self, data_to_add):
        """Добавление данных в JSON файл."""
        pass

    @abstractmethod
    def del_from_json(self, item_id):
        """Удаление данных из JSON файла."""
        pass


class WorkingWithData(BaseData):
    """
    Класс для работы с файлами.
    """

    def __init__(self, filepath="data/data.json"):
        self.filepath = filepath

    def read_json(self):
        """
        Метод для чтения файла.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_to_json(self, data_to_add):
        """
        Метод для добавления информации в файл.
        """
        existing_data = self.read_json()

        if isinstance(data_to_add, dict):
            existing_data.append(data_to_add)

        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)

    def del_from_json(self, item_id):
        """
        Метод для удаления данных из файла и перезаписи.
        """
        new_data = self.read_json()
        new_data = [data for data in new_data if data.get("id") != item_id]

        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)
