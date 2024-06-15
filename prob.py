import json


def parse_pages(categories):
    with open('pages.json', 'r') as f:
        pages = json.load(f)

    if categories == 'all':
        categories = pages.keys()
        print(categories)
        for category in categories:
            if category in pages:
                print(f"Parsing category: {category}")
                for url in pages[category]:
                    html = url
                    print(html)
            else:
                print(f"Category {category} not found in pages_to_parse.json")
    else:
        for category in categories.split(','):
            if category in pages:
                print(f"Parsing category: {category}")
                for url in pages[category]:
                    html = url
                    print(html)
            else:
                print(f"Category {category} not found in pages_to_parse.json")

print("Какие категории вы хотите пропарсить?\ndiodes - Диоды\nthyristors - Тиристоры\npower-ics - Силовые микросхемы\nanalog-switches - Аналоговый переключатели\nmosfets - Металл–оксид–полупроводник\noptocouplers - Оптосоединители\nrelays - реле\nreceiver - Приемники\nleds - Светильники\nphoto-detectors - Фото-детектеры\nir-em\ndisplays - Дисплеи\nmodules - модульные\ncapacitors - Конденсаторы\nresistors - Резисторы\n")
inputer = input()
parse_pages(inputer)
#return 0
