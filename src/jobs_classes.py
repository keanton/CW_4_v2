class Vacancy:
    __slots__ = ('__name', '__url', '__description', '__payment')
    def __init__(self, name: str, url: str, description: str, payment: str):
        if int(payment) < 0:
            raise ValueError("Payment cannot be negative")
        self.__name = name
        self.__url = url
        self.__description = description    #Описание вакансии
        self.__payment = payment

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def description(self):
        return self.__description

    @property
    def payment(self):
        return self.__payment

    def __str__(self):
        return f"Name: {self.__name}, Url: {self.__url}, Description: {self.__description}, Payment: {self.__payment}"

    def __lt__(self, other):
        return int(self.__payment) < int(other.__payment)

    def __le__(self, other):
        return int(self.__payment) <= int(other.__payment)

class FileOperations:
    def __init__(self, vacancies, filter_words=None, top_count=0):
        self._vacancies = vacancies
        self.filter_words = filter_words
        self.top_count = top_count
        self.list_vacancies = []

    def filter_vacancies(self):
        """
        Функция фильтрации вакансий по ключевым словам пользователя
        :param vacancies:
        :param filter_words:
        :return:
        """
        for i in self._vacancies:
            if i['description'] is not None:
                if self.filter_words.lower() in i['description'].lower():
                    self.list_vacancies.append(i)
        return self.list_vacancies

    def sorting(self):
        """
        Сортировка вакансий по зарплате
        :param vacancies:
        :return:
        """
        sorted_data = sorted(self._vacancies, key=lambda x: self.get_avg_salary_range(x['payment']), reverse=True)
        return sorted_data

    def get_avg_salary_range(self, payment):
        """
        Функция для получения среднего значения зарплаты из диапазона
        """
        if type(payment) != int:
            if payment['currency'] == 'USD':    #Переводим доллар в рубли(пока так)
                if payment['to'] is not None:
                    payment['to'] *= 80
                if payment['from'] is not None:
                    payment['from'] *= 80
                payment['currency'] = 'RUR(from USD(80))'
            if payment['currency'] == 'EUR':
                if payment['to'] is not None:
                    payment['to'] *= 85
                if payment['from'] is not None:
                    payment['from'] *= 85
                payment['currency'] = 'RUR(from EUR(85))'
            if payment['currency'] == 'KZT':
                if payment['to'] is not None:
                    payment['to'] *= 0.15
                if payment['from'] is not None:
                    payment['from'] *= 0.15
                payment['currency'] = 'RUR(from KZT(0,15))'
            if payment['to'] == None:
                return payment['from']
            if payment['from'] == None:
                return payment['to']
            return (payment['to'] + payment['from']) / 2    # Считаем среднее значение зарплаты из значений to и from
        else:
            return payment

    def get_top(self):
        """
        Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods)
        """
        top = []
        counter = 0
        for v in self._vacancies:
            if counter < self.filter_words:
                top.append(v)
                counter +=1
            else:
                break
        return top