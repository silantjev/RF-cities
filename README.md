# goroda
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


Используемые модули:
os, pandas, tkinter, geopy

Файлы с расширением py следует запускать программой-интерпретатором python3, например:
python3 trucker.py
или
python trucker.py

Для установки Python см. https://www.python.org/downloads/
На ubuntu:
sudo apt-get install python3

Также необходимо установить модули:
pip install pandas tk geopy
