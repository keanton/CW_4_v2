from src.engine_classes import HH, SuperJob
from src.jobs_classes import Vacancy, FileOperations
from src.json_class import JSONSaver


def platforms():
    """
    Функция выбора платформы
    :return:
    """
    print("Выберите платформу для поиска вакансии: \nВведите цифру '1' для Hh.ru\nВведите цифру '2' для Superjob.ru\nВведите цифру '3' для всех доступных платформ")
    #return 3
    while True:
        platform = input()
        if platform == '1':
            print('Вы выбрали платформу Hh.ru')
            return 1
        elif platform == '2':
            print('Вы выбрали платформу Superjob.ru')
            return 2
        elif platform == '3':
            print('Вы выбрали все доступные программе платформы ')
            return 3
        else:
            print("Неверное значение! Введите цифру от 1-3!")

def search_query():
    """
    Функция получения поискового запроса
    :return:
    """
    return input("Введите поисковый запрос: ")
    #return "java"

def get_user_request():
    """
    Функция поиска заданного запроса на выбранной платформе
    :return:
    """
    u_p = platforms()
    s_q = search_query()
    if u_p == 1:
        hh = HH(s_q)    #hh = HH(search_query)
        hh_vacancies = hh.get_request()
        return hh.get_request()
    elif u_p == 2:
        sj = SuperJob(s_q)    #sj = SuperJob(search_query)
        return sj.get_request()
    elif u_p == 3:
        hh = HH(s_q)
        hh_vacancies = hh.get_request()
        sj = SuperJob(s_q)
        sj_vacancies = sj.get_request()
        return hh_vacancies + sj_vacancies

def work_with_file(vacancies):
    """
    Функция вывода второго меню, где пользователь взаимоджействует с полученными данными
    :param vacancies:
    :return:
    """
    while True:
        print("Меню работы с данными: \nНажмите '1', если хотите сохранить файл и выйти\nНажмите '2' для фильтрации вакансий по ключевому слову\nНажмите '3' для сортировке вакансий по зп\nНажмите '4' для отсортировки топ N-количества вакансий(задаете сами)")

        user = input()
        #user = '1'
        if user == '1':
            return vacancies
        elif user == '2':
            filter_words = input("Введите ключевое слово для фильтрации вакансий: ")
            #filter_words = "django"
            vacancies = FileOperations(vacancies, filter_words, top_count=0).filter_vacancies()   #Фильтрация вакансий по ключевому слову
            if not vacancies:
                print("Нет вакансий, соответствующих заданным критериям.")
                return
            print("Операция выполнена!")
        elif user == '3':
            vacancies = FileOperations(vacancies).sorting()    #Сортировка полученных данных
            print("Операция выполнена!")
        elif user == '4':
            while True:
                try:
                    top_count = float(input("Введите количество вакансий: "))
                    vacancies = FileOperations(vacancies, top_count).get_top()  # Отсортировка топ N-количества вакансий
                    print("Операция выполнена!")
                    break
                except ValueError:
                    print("Вы ввели не число. Пожалуйста, попробуйте снова.")
        else:
            print("Неверное значение! Введите цифру от 1 - 4!")

def check_vacancies_data():
    """
    Функция проверки найденных по запросу вакансий
    :return:
    """
    while True:
        vacancies_data = get_user_request()    #Список вакансий по запросу пользователя
        for v in vacancies_data:
            if v is not None:
                return vacancies_data
        print("Ваш запрос не найден на платформе! ")


def main():
    print("Привествую! Это программа по парсингу и обработке данных с сайта вакансий hh.ru  superjob.ru")
    vacancies_data = check_vacancies_data()
    json_saver = JSONSaver(vacancies_data)
    json_saver.add_vacancies()
    vacancies = json_saver.data_file()
    user_vacancies = work_with_file(vacancies)
    JSONSaver(user_vacancies).get_user_file()
    print("Данные сохранены и записаны в файл 'user_data.json'")
    vacancy = Vacancy("Специалист", "<https://hh.ru/vacancy/123456>", "Требования: опыт работы от 3 лет...", "100000")
    #JSONSaver("data_file.json").add_vacancy(vacancy)
    #JSONSaver("data_file.json").delete_vacancy(vacancy)