# test-assignment-effective-mobile
Автор: Андрей Скуридин aka andrzej-skuridin

### Задача:
Реализовать телефонный справочник со следующими возможностями:
1. Вывод постранично записей из справочника на экран
2. Добавление новой записи в справочник
3. Возможность редактирования записей в справочнике
4. Поиск записей по одной или нескольким характеристикам

Плюсом будет:
1. Аннотирование функций и переменных
2. Документирование функций
3. Подробно описанный функционал программы
4. Размещение готовой программы и примера файла с данными на github

#### Технические требования:
1. Реализация интерфейса через консоль (без веб- или графического интерфейса)
2. Хранение данных должно быть организовано в виде текстового файла, формат которого придумывает сам программист
3. В справочнике хранится следующая информация: фамилия, имя, отчество, название организации, телефон рабочий, телефон личный (сотовый)

#### Запуск (при работе в Linux):

1) Перейти в каталог проекта
2) Установить виртуальное окружение: ```python3 -m venv venv```
3) Установить зависимости: ```pip3 install -r requirements.txt```
4) Запустить: ```python3 main.py```

#### Запуск (при работе в Windows):

1) Перейти в каталог проекта
2) Установить виртуальное окружение: ```python -m venv venv```
3) Установить зависимости: ```pip install -r requirements.txt```
4) Запустить: ```python main.py```

### Реализация:
Техническое задание реализовано в полном объёме. Хранение данных осуществляется в 
текстовом файле (.txt), взаимодействие с ним - через БД TinyDB.
Инструкции по работе со справочником выводятся в консоли при переходе между меню. 
Предусмотрены ситуации с вводом неверных команд.

P.S. Пришлите обратную связь, пожалуйста.