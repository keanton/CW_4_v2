from abc import ABC, abstractmethod
from src.auth_data import token
import requests


class Engine(ABC):
    def __init__(self, search_query: str) -> None:
        self._search_query = search_query
        self._per_page = 100


    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):
    def __init__(self, search_query: str):
        super().__init__(search_query)
        self.vacancies_data = []
        self.url = "https://api.hh.ru/vacancies"
        self.params = {"text": self._search_query, "per_page": self._per_page}

    def get_request(self) -> list:
        """
        Функция парсинга данных с HH
        :return:
        """
        response = requests.get(self.url, self.params)
        if response.status_code == 200:
            vacancies = response.json()["items"]
            for vacancy in vacancies:
                if vacancy['salary'] is not None:
                    vacancy_data = {'name': vacancy['name'], 'url': vacancy['url'],
                                    'description': vacancy['snippet']['requirement'], 'payment': vacancy['salary']}
                    self.vacancies_data.append(vacancy_data)
                else:
                    continue
        else:
            print("Error:", response.status_code)
        return self.vacancies_data


class SuperJob(Engine):
    def __init__(self, search_query: str):
        super().__init__(search_query)
        self.vacancies_data = []
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.headers = {'X-Api-App-Id': token}   #token -> api_key
        self.params = {'keyword': self._search_query, 'page': 1, 'count': self._per_page}

    def get_request(self) -> list:
        """
        Функция парсинга данных с SJ
        :return:
        """
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            vacancies = response.json()["objects"]
            for vacancy in vacancies:
                vacancy_data = {'name': vacancy['profession'], 'url': vacancy['link'], 'description': vacancy['candidat'], 'payment': vacancy['payment_from']}
                self.vacancies_data.append(vacancy_data)
        #vacancy['candidat'] описание
        #vacancy['payment_from'] зарплата
        else:
            print("Error:", response.status_code)
        return self.vacancies_data