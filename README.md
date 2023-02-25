# RF cities
Несколько приложений, работающих с данными о российских городах.
Цель проекта — тренировка написания приложений на языке Python.

Язык: Python 3

Автор: А. В. Силантьев

Файлы:
trucker.py — графическая версия игры "торговец-дальнобойщик";
console_trucker.py — консольная версия игры "торговец-дальнобойщик";
info_about_cities.py — приложение, которое сообщает координаты города по названию;
cities.py — модуль с функциями для игры "торговец-дальнобойщик";
goroda.csv — файл с данными о городах РФ (2022);
requirements.txt — файл с необходимыми библиотеками для всего проекта
Dockerfile используется для создания образа приложения console_trucker


Используемые модули:
os, tkinter, pandas=1.5.2, geopy=2.3.0

Файлы с расширением py следует запускать программой-интерпретатором python3, например:
python3 trucker.py
или
python trucker.py

Для установки Python см. https://www.python.org/downloads/
На ubuntu:
sudo apt-get install python3

Также необходимо установить модули:
pip install pandas geopy
или
pip install -r requirements.txt


Команды для docker.

-Создание образа:
docker build -t trucker .

-Запуск:
docker run -i --rm --name console_trucker trucker

-Остановка:
docker stop console_trucker
