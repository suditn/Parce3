main.py - Парсинг сайта\n
csv_datasheet.py - Создание локальных json и csv
pages.json - Страницы которые парсяца

main.py:
Запускает парсер. Можно качать один, несколько файлов через запятую или все написав all. Варианты написаны при запуске.
Библиотеки:
os
re
time
json
pathlib
logging
requests
bs4
pandas
asyncio
aiohttp
aiofiles
selenium
concurrent
opencv-python

csv_datasheet.py:
Делает json и csv в локальных папках по общим csv. Выбирать как создавать так же как и в main.py.
