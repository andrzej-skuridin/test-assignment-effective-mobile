# by andrzej-skuridin
# Python 3.11

import json
import math
import sys

from tinydb import TinyDB, Query

FIELDS = ('family_name',
          'first_name',
          'patronymic',
          'organization',
          'work_number',
          'personal_number'
          )

db = TinyDB('db.txt')


def subscriber_exists(family_name: str,
                      first_name: str,
                      patronymic: str) -> bool:
    """Проверяет наличие абонента в телефонном справочнике."""
    if len(db.search(Query().fragment({'family_name': family_name,
                                       'first_name': first_name,
                                       'patronymic': patronymic})
                     )) > 0:
        return True
    return False


def insert_subscriber() -> None:
    """Внести нового пользователя в телефонный справочник.
    Считается, что все поля обязательные, ограничений на вводимые данные нет."""

    family_name = input('Введите фамилию: ')
    first_name = input('Введите имя: ')
    patronymic = input('Введите отчество: ')
    organization = input('Введите название организации: ')
    work_number = input('Введите рабочий телефон: ')
    personal_number = input('Введите личный телефон: ')

    if not subscriber_exists(family_name=family_name,
                             first_name=first_name,
                             patronymic=patronymic, ):
        db.insert({'family_name': family_name,
                   'first_name': first_name,
                   'patronymic': patronymic,
                   'organization': organization,
                   'work_number': work_number,
                   'personal_number': personal_number,
                   }
                  )
    else:
        print('Такой пользователь уже существует!')


def find_subscriber() -> None:
    """Выводит данные об определённом пользователе."""

    lookout_fields = []
    print('Введите название поля, по которому будет проводиться поиск.\n'
          'Если полей поиска несколько, вводите по одному за раз.\n'
          'Поля: family_name, first_name, patronymic, organization, '
          'work_number, personal_number.\n'
          'Введите /stop, если хотите прекратить ввод полей.\n')
    while True:
        lookout_field = input('>> ')
        if lookout_field == '/stop':
            break
        elif lookout_field not in FIELDS:
            print('Такого поля не существует!')
        elif lookout_field in lookout_fields:
            print('Это поле уже внесено в поисковый список!')
        else:
            lookout_fields.append(lookout_field)

    if len(lookout_fields) != 0:
        vals = dict()
        for field in lookout_fields:
            print(f'Введите поисковое значение для поля {field}.')
            val = input('>> ')
            vals[field] = val
        subscribers = json.loads(json.dumps(db.search(Query().fragment(vals))))
        sorted_subscribers = sorted(subscribers,
                                    key=lambda x: (x['family_name'],
                                                   x['first_name'],
                                                   x['patronymic']))
        for subscriber in sorted_subscribers:
            print(f'Фамилия: {subscriber["family_name"]}\n'
                  f'Имя: {subscriber["first_name"]}\n'
                  f'Отчество: {subscriber["patronymic"]}\n'
                  f'Организация: {subscriber["organization"]}\n'
                  f'Рабочий номер: {subscriber["work_number"]}\n'
                  f'Личный номер: {subscriber["personal_number"]}\n'
                  )
    else:
        print('Не обнаружено полей для поиска. Поиск прерван.')


def update_subscriber() -> None:
    """Изменить данные о пользователе в телефонном справочнике."""

    print('Введите ФИО редактируемого пользователя.')
    family_name = input('Введите фамилию: ')
    first_name = input('Введите имя: ')
    patronymic = input('Введите отчество: ')
    if subscriber_exists(family_name=family_name,
                         first_name=first_name,
                         patronymic=patronymic, ):
        switch = '1'
        while switch != '/exit':
            print('Введите название поля, которое хотите отредактировать.\n'
                  'Поля: family_name, first_name, patronymic, organization, '
                  'work_number, personal_number.\n'
                  'Введите /exit, если хотите выйти из редактора.\n')
            if switch == '/exit':
                break
            switch = input('>> ')
            if switch in FIELDS:
                print(f'Введите новое значения для поля {switch}: ')
                new_value = input()
                db.update(fields={switch: new_value},
                          cond=Query().fragment({'family_name': family_name,
                                                 'first_name': first_name,
                                                 'patronymic': patronymic})
                          )
            elif switch not in FIELDS and switch != '/exit':
                print('Такого поля не существует!')
    else:
        print('Абонент не найден!')


def list_all_subscribers() -> None:
    """Вывести список всех абонентов."""
    subscribers = json.loads(json.dumps(db.all()))
    sorted_subscribers = sorted(subscribers,
                                key=lambda x: (x['family_name'],
                                               x['first_name'],
                                               x['patronymic']))

    subscribers_amount = len(sorted_subscribers)
    print(f'Абонентов в телефонном справочнике: {subscribers_amount}.')

    for subscriber in sorted_subscribers:
        print(f'Фамилия: {subscriber["family_name"]}\n'
              f'Имя: {subscriber["first_name"]}\n'
              f'Отчество: {subscriber["patronymic"]}\n'
              f'Организация: {subscriber["organization"]}\n'
              f'Рабочий номер: {subscriber["work_number"]}\n'
              f'Личный номер: {subscriber["personal_number"]}\n'
              )


def paginate(items: list, page_size: int, page_number: int) -> list:
    """Разбивает список абонентов по страницам."""

    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    return items[start_index:end_index]


def paginated_list_subscribers() -> None:
    """Выводит список абонентов постранично."""

    subscribers = json.loads(json.dumps(db.all()))
    print('Введите число абонентов на странице (положительное число).')
    try:
        n_subs = int(input('>> '))
    except ValueError:
        print('Это не число. Будет выведен 1 абонент на страницу.')
        n_subs = 1
    if n_subs < 1:
        print('Отрицательные числа не годятся. Будет выведен 1 абонент на страницу.')
        n_subs = 1

    while True:
        print(f'Число страниц в справочнике: {math.ceil(len(subscribers) / n_subs)}.')
        print('Введите номер страницы телефонного справочника (положительное число).\n'
              'Введите 0, чтобы прекратить просмотр.')
        try:
            page = int(input('>> '))
        except ValueError:
            print('Это не число. Будет открыта первая страница.')
            page = 1
        if page == 0:
            break
        elif page > 0:
            sorted_subscribers = sorted(subscribers,
                                        key=lambda x: (x['family_name'],
                                                       x['first_name'],
                                                       x['patronymic']))
            for subscriber in paginate(items=sorted_subscribers,
                                       page_size=n_subs,
                                       page_number=page):
                print(f'Фамилия: {subscriber["family_name"]}\n'
                      f'Имя: {subscriber["first_name"]}\n'
                      f'Отчество: {subscriber["patronymic"]}\n'
                      f'Организация: {subscriber["organization"]}\n'
                      f'Рабочий номер: {subscriber["work_number"]}\n'
                      f'Личный номер: {subscriber["personal_number"]}\n'
                      )


COMMANDS = {
    0: sys.exit,
    1: list_all_subscribers,
    2: paginated_list_subscribers,
    3: insert_subscriber,
    4: update_subscriber,
    5: find_subscriber
}

if __name__ == '__main__':
    while True:
        print('Введите команду:\n'
              '0 - завершить работу\n'
              '1 - отобразить всех абонентов в справочнике\n'
              '2 - отобразить абонентов в справочнике постранично\n'
              '3 - внести нового абонента в адресную книгу\n'
              '4 - отредактировать данные об абоненте\n'
              '5 - поиск абонентов в справочнике')

        try:
            command = int(input('>> '))
        except ValueError:
            print('Это не число. Введите число от 1 до 5.')
            continue

        if command in COMMANDS:
            COMMANDS[command]()
        else:
            print('Неизвестная команда!')
