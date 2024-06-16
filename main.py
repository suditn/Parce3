import os
import re
import time
import json
from pathlib import Path
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import aiohttp
import aiofiles
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from concurrent.futures import ThreadPoolExecutor
#

# Логи
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Поиск слова

pattern = re.compile(r'\w+')

# Настройка браузера ссылок и путей файлов
options = Options()

options.headless = True
driver = webdriver.Edge(options=options)
url = 'https://www.vishay.com/en'
save_path = str(Path(__file__).parent.resolve())
print(save_path)
img_small_save_path = os.path.join(save_path, "image")
print(img_small_save_path)
datasheet_save_path = os.path.join(save_path, "Datasheet")
headers = {'User-Agent': "scrapping_script/1.0"}
'''
---capacitors---
--aluminum--
"/capacitors/aluminum/"
--ceramic--
"/capacitors/ceramic/ceramic-multilayer-smd/","/capacitors/ceramic/ceramic-multilayer-leaded/","/capacitors/ceramic/ceramic-singlelayer/", "/capacitors/ceramic/high-voltage/", "/capacitors/ceramic/ceramic-rf-power/"
"/capacitors/energy-storage/", "/capacitors/film/", "/capacitors/polymer/"
"/capacitors/power-heavy-current/high-voltage-ac/", "/capacitors/power-heavy-current/surge-suppressor/", "/capacitors/power-heavy-current/unbalance-monitoring/", "/capacitors/power-heavy-current/medium-line-frequency/", "/capacitors/power-heavy-current/low-voltage-ac/", "/capacitors/power-heavy-current/power-electronic-ac-dc/", "/capacitors/power-heavy-current/power-factor-controllers/"
"/capacitors/tantalum/", "/capacitors/thin-film/", "/capacitors/custom-capacitors/"

---RESISTORS---
--fixed--
"/resistors-fixed/", "/networks-and-arrays/"
"/thermistors/ntc/", "/thermistors/ptc/", "/thermistors/rtd/"
"/varistors/", "/trimmers/", "/rheostats/", "/potentiometers/", "/resistors-fixed/custom-capabilities/"


"/diodes/tvs-protection/", "/diodes/esd-protection/", "/diodes/emi-filter/", "/diodes/zener-stabilizers/",
          "/diodes/switching/", "/diodes/ss-schottky/", "/diodes/standard-recovery/", "/diodes/ultrafast-recovery/",
          "/diodes/schottky/", "/diodes/bridge/","/diodes/med-high-diodes/", "/thyristors/phase-control-discrete/", "/power-ics/integrated-microbuck/", "/power-ics/integrated-microbrick/", "/power-ics/integrated-drmos/", "/power-ics/slew-rate-control/", "/power-ics/current-limiter/", "/power-ics/true-bi-directional/", "/power-ics/integrated-OR-ing-switch/", "/power-ics/automotive/", "/power-ics/computer/", "/power-ics/consumer/", "/power-ics/healthcare/", "/power-ics/industrial/", "/power-ics/networking/", "/power-ics/portables/", "/power-ics/motor-drive/", "/power-ics/battery-and-protection/", "/power-ics/precision-logic-switch/",
          

"/mosfets/",
"/analog-switches/", "/optocouplers/opt-tran-output/", "/optocouplers/opto-darl-out/", "/optocouplers/opto-ac-in/", "/optocouplers/opto-triac/", "/optocouplers/opto-linear/", "/optocouplers/opto-high-speed/", "/optocouplers/opto-driver/", "/solid-state-relays/", "/ir-receiver-modules/", "/leds/standards/", "/leds/power/", "/leds/bicolor/", "/leds/rgb/", "/photo-detectors/surface-mount-devices/", "/photo-detectors/leaded-devices/", "/ir-emitting-diodes/", "/ir-transceivers/", "/displays/seven-segment-display/", "/displays/lcd-character/", "/displays/lcd-graphic/", "/displays/oled-character/", "/displays/oled-graphic/", "/displays/color-tft-display/", "/displays/seven-segment-display/"
"/modules/bridge-modules/", "/modules/diode-modules/fred/",  "/modules/diode-modules/high-performance-schottky/", "/modules/diode-modules/fast-diode/", "/modules/diode-modules/high-voltage/"]

'''
# Список используемых ссылок
sl_use = []
# Список неудавшихся загрузок
failed_downloads = []



# Создание папок
def create_directories(sl):
    Path(img_small_save_path, sl).mkdir(parents=True, exist_ok=True)
    Path(datasheet_save_path, sl).mkdir(parents=True, exist_ok=True)

# Выгрузка полной таблицы на страницу
def get_web(u, sl):
    driver.get(u)
    logging.info(f'Открыта страница: {u}')
    create_directories(sl)
    wait = WebDriverWait(driver, 10)
    option = driver.find_element('xpath', '//label/select/option[1]')
    option_max = driver.find_element('xpath', '//label/select/option[4]')
    try:
        max_entries = driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[3]/div[1]/div').text
        driver.execute_script('arguments[0].value = arguments[1]', option, pattern.findall(max_entries)[5])
        option.click()
        print(1)
    except:
        try:
            max_entries = driver.find_element('xpath','/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[1]/div[1]/div').text
            driver.execute_script('arguments[0].value = arguments[1]', option, pattern.findall(max_entries)[5])
            option.click()
            print(1)
        except :
            try:
                max_entries = driver.find_element('xpath','/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div/div[1]/div[1]/div').text
                driver.execute_script('arguments[0].value = arguments[1]', option, pattern.findall(max_entries)[5])
                option.click()
                print(1)
            except :
                try:
                    max_entries = driver.find_element('xpath','/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[1]/div[1]/div').text
                    driver.execute_script('arguments[0].value = arguments[1]', option, pattern.findall(max_entries)[5])
                    option.click()
                    print(1)
                except:
                    max_entries = driver.find_element('xpath','/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div[3]/div[1]/div').text
                    driver.execute_script('arguments[0].value = arguments[1]', option, pattern.findall(max_entries)[5])
                    option.click()
                    print(1)

    return driver.page_source

async def download_file_with_retry(session, url, path, file_3d_pr, headers=None):
    await asyncio.sleep(60)
    retries = 10
    for attempt in range(retries):
        try:
            #with time.sleep(5):
            await asyncio.sleep(5)
            async with session.get(url, headers=headers, timeout=60) as response:
                response.raise_for_status()
                file_dir = os.path.dirname(path)
                Path(file_dir).mkdir(parents=True, exist_ok=True)
                if not os.path.exists(path):
                    async with aiofiles.open(path, 'wb') as out_file:
                        await out_file.write(await response.read())
                    logging.info(f'Файл {os.path.basename(path)} успешно загружен и сохранен.')
                    response.close()
                else:
                    logging.info(f'Файл {os.path.basename(path)} уже существует.')
                    #datasheet_src.append(path.split("/")[1::])
                    file_3d_pr = True
                    #session.close()
                return True
        except Exception as e:
            if e[:3] == '404':
                print(e[:3])
                continue
            else:
                logging.error(f'Ошибка при загрузке файла {url}: {e[:3]}')
                logging.info(f'Повторная попытка загрузки файла {url}... (попытка {attempt + 1}/{retries})')
                await asyncio.sleep(30)
                continue
    logging.error(f'Не удалось загрузить файл {url} после {retries} попыток.')
    failed_downloads.append(url)
    return False

async def download_image_with_retry(session, url, path, headers=None):
    await asyncio.sleep(60)
    retries = 10
    for attempt in range(retries):
        try:
            await asyncio.sleep(5)
            async with session.get(url, headers=headers, timeout=60) as response:
                response.raise_for_status()
                file_dir = os.path.dirname(path)
                Path(file_dir).mkdir(parents=True, exist_ok=True)
                if not os.path.exists(path):
                    async with aiofiles.open(path, 'wb') as out_file:
                        await out_file.write(await response.read())
                    logging.info(f'Изображение {os.path.basename(path)} успешно загружено и сохранено.')
                else:
                    logging.info(f'Изображение {os.path.basename(path)} уже существует.')
                return True
        except Exception as e:
            if e[:3] == '404':
                print(e[:3])
                continue
            else:
                logging.error(f'Ошибка при загрузке изображения {url}: {e[:3]}')
                logging.info(f'Повторная попытка загрузки изображения {url}... (попытка {attempt + 1}/{retries})')
                await asyncio.sleep(30)
                continue
    logging.error(f'Не удалось загрузить изображение {url} после {retries} попыток.')
    failed_downloads.append(url)
    return False

async def download_3d_model_with_retry(session, img_alt, file_3d_path, file_3d_pr, file_3d_src):
    await asyncio.sleep(60)
    retries = 10
    for attempt in range(retries):
        try:
            await asyncio.sleep(5)
            async with session.get('https://www.vishay.com/en/product/' + img_alt + '/tab/designtools-ppg/', headers=headers, timeout=60) as response:
                logging.info(f'Загрузка 3D модели: https://www.vishay.com/en/product/{img_alt}/tab/designtools-ppg/')
                response.raise_for_status()
                if response.status == 200:
                    soupp = BeautifulSoup(await response.text(), "lxml")
                    file_3d_cont = [a['href'] for a in soupp.findAll('a', href=True) if a['href'].endswith('.zip') or a['href'].endswith('.txt')]
                    logging.info(f'Найдено {len(file_3d_cont)} файлов 3D моделей для продукта {img_alt}')
                    for b in file_3d_cont:
                        if b.endswith('.zip'):
                            logging.info(f'Загрузка файла 3D модели: {b}')
                            file_3d_pr = True
                            return await download_file_with_retry(session, 'https://www.vishay.com' + b, file_3d_path, file_3d_pr, headers)
            return False
        except aiohttp.ClientError as e:
            logging.error(f'Ошибка при получении 3D модели для продукта {img_alt}: {e}')
            await asyncio.sleep(30)
        except asyncio.TimeoutError:
            logging.error(f'Тайм-аут при получении 3D модели для продукта {img_alt}')
            await asyncio.sleep(30)
        logging.info(f'Повторная попытка загрузки 3D модели {img_alt}... (попытка {attempt + 1}/{retries})')
    logging.error(f'Не удалось загрузить 3D модель {img_alt} после {retries} попыток.')
    failed_downloads.append('https://www.vishay.com/en/product/' + img_alt + '/tab/designtools-ppg/')
    return False

async def process_html(session, html_source, sl):
    soup = BeautifulSoup(html_source, "lxml")
    table = soup.find('table', {'id': 'poc'})
    pdff = table.findAll('div', {'class':'Webtable_vshPdfLnk__394JH'})

    images = table.findAll('img')
    columns = [i.get_text(strip=True) for i in table.find_all("th")]
    data = [[td.get_text(strip=True) for td in tr.find_all("td")] for tr in table.find("tbody").find_all("tr")]
    df = pd.DataFrame(data, columns=columns)
    if pdff == []:
        pdff = table.findAll('div', {'class':'Table_vshPdfLnk__2Cd7D'})
    pdf = [p.find('a').get('href') for p in pdff]
    img_src = []
    datasheet_src = []
    datasheet_pr = False
    file_3d_src = []
    #img_path = ""
    #datasheet_path = ""
    #file_3d_path = ""
    previous_img_src = ''
    previous_datasheet_src = ''
    i = 0

    tasks = []

    for img in images:
        series = df[columns[0]][i]
        if img['src'].split('/')[-2] == 'pt-small':
            try:
                img_filename = img['alt'] + '.png'
            except KeyError:
                img_filename = (img['src'].split('/')[-1]).split('-')[0] + '.png'
            try:
                if (sl.split('/')[-4] != ""):
                    img_src.append("image" + "\\" + sl.split('/')[-4] + "\\" + img_filename)
                    img_path = os.path.join(img_small_save_path + "/" + sl.split('/')[-4] + "\\", img_filename)
                elif (sl.split('/')[-3] != ""):
                    img_src.append("image" + "/" + sl.split('/')[-3] + "\\" + img_filename)
                    img_path = os.path.join(img_small_save_path + "\\" + sl.split('/')[-3] + "\\", img_filename)
                else:
                    img_src.append("image" + sl + img_filename)
                    img_path = os.path.join(img_small_save_path + sl, img_filename)
            except IndexError:
                if(sl.split('/')[-3] != ""):
                    img_src.append("image" + "\\" + sl.split('/')[-3] + "\\" + img_filename)
                    img_path = os.path.join(img_small_save_path + "\\" + sl.split('/')[-3] + "\\", img_filename)
                else:
                    img_src.append("image" + sl + img_filename)
                    img_path = os.path.join(img_small_save_path + sl, img_filename)


            if previous_img_src != img['src'] and (img['src'].split('/')[-1]).split('-')[0] != "Datasheet":
                try:
                    tasks.append(download_image_with_retry(session, 'https://www.vishay.com/' + img['src'], img_path, headers))
                except KeyError:
                    tasks.append(download_image_with_retry(session, 'https://www.vishay.com/' + (img['src'].split('/')[-1]).split('-')[0], img_path, headers))
                previous_img_src = img['src']

            datasheet_filename = series + '.pdf'
            file_3d_name = series + '.zip'
            #print(sl.split('/')[-4])
            try:
                if (sl.split('/')[-4] != ""):
                    datasheet_path = os.path.join(datasheet_save_path + "\\" + sl.split('/')[-4] + "\\", series, datasheet_filename)
                    file_3d_path = os.path.join(datasheet_save_path + "\\" + sl.split('/')[-4] + "\\", series, file_3d_name)
                elif (sl.split('/')[-3] != ""):
                    datasheet_path = os.path.join(datasheet_save_path + "\\" + sl.split('/')[-3] + "\\", series, datasheet_filename)
                    file_3d_path = os.path.join(datasheet_save_path + "\\" + sl.split('/')[-3] + "\\", series, file_3d_name)
                else:
                    datasheet_path = os.path.join(datasheet_save_path + "\\" + sl, series, datasheet_filename)
                    file_3d_path = os.path.join(datasheet_save_path + "\\" + sl, series, file_3d_name)
            except IndexError:
                if (sl.split('/')[-3] != ""):
                    datasheet_path = os.path.join(datasheet_save_path + "\\" + sl.split('/')[-3] + "\\", series, datasheet_filename)
                    file_3d_path = os.path.join(datasheet_save_path + "\\" + sl.split('/')[-3] + "\\", series, file_3d_name)
                else:
                    datasheet_path = os.path.join(datasheet_save_path + "\\" + sl, series, datasheet_filename)
                    file_3d_path = os.path.join(datasheet_save_path + "\\" + sl, series, file_3d_name)

            file_3d_pr = False
            if previous_datasheet_src != series:

                try:
                    tasks.append(download_file_with_retry(session, 'https://www.vishay.com/doc?' + img['alt'], datasheet_path, file_3d_pr, headers))
                except KeyError:
                    tasks.append(download_file_with_retry(session, 'https://www.vishay.com/doc?' + (img['src'].split('/')[-1]).split('-')[0], datasheet_path,file_3d_pr, headers))
                try:
                    tasks.append(download_3d_model_with_retry(session, img['alt'], file_3d_path, file_3d_pr, file_3d_src))
                except KeyError:
                    tasks.append(download_3d_model_with_retry(session, (img['src'].split('/')[-1]).split('-')[0], file_3d_path, file_3d_pr, file_3d_src))
                datasheet_src.append(datasheet_path[10::])
            else:
                datasheet_src.append(datasheet_path[10::])


            previous_datasheet_src = series
            i += 1


    if i != len(pdf):
        i = 0
        for p in pdf:
            series = df[columns[0]][i]
            datasheet_filename = series + '.pdf'
            file_3d_name = series + '.zip'
            #print(p)
            img_src.append(p.split('?')[1])
            print(sl.split('/')[-3])
            try:
                if (sl.split('/')[-4] != ""):
                    datasheet_path = os.path.join(datasheet_save_path + "/" + sl.split('/')[-4] + "/", series, datasheet_filename)
                    file_3d_path = os.path.join(datasheet_save_path + "/" + sl.split('/')[-4] + "/", series, file_3d_name)
                elif (sl.split('/')[-3] != ""):
                    datasheet_path = os.path.join(datasheet_save_path + "/" + sl.split('/')[-3] + "/", series, datasheet_filename)
                    file_3d_path = os.path.join(datasheet_save_path + "/" + sl.split('/')[-3] + "/", series, file_3d_name)
                else:
                    datasheet_path = os.path.join(datasheet_save_path + "/" + sl, series, datasheet_filename)
                    file_3d_path = os.path.join(datasheet_save_path + "/" + sl, series, file_3d_name)
            except IndexError:
                if (sl.split('/')[-3] != ""):
                    datasheet_path = os.path.join(datasheet_save_path + "/" + sl.split('/')[-3] + "/", series, datasheet_filename)
                    file_3d_path = os.path.join(datasheet_save_path + "/" + sl.split('/')[-3] + "/", series, file_3d_name)
                else:
                    datasheet_path = os.path.join(datasheet_save_path + "/" + sl, series, datasheet_filename)
                    file_3d_path = os.path.join(datasheet_save_path + "/" + sl, series, file_3d_name)

            file_3d_pr = False
            if previous_datasheet_src != series:
                tasks.append(download_file_with_retry(session, 'https://www.vishay.com' + p, datasheet_path, file_3d_pr, headers))
                tasks.append(download_3d_model_with_retry(session, p.split('?')[1], file_3d_path, file_3d_pr, file_3d_src))
                datasheet_src.append(datasheet_path[10::])
            else:
                datasheet_src.append(datasheet_path[10::])
            previous_datasheet_src = series
            i += 1
    await asyncio.gather(*tasks, return_exceptions=True)
    print(os.path.isfile(file_3d_path))
    print(file_3d_path)

    return df, img_src, datasheet_src

def save_to_excel(df, img_src,datasheet_src, file_3d_src, save_path, url):
    # Удаляем столбец "Buy Now" если он существует
    if 'Buy Now' in df.columns:
        df = df.drop(columns=['Buy Now'])
    excel_path = os.path.join(save_path + "/exclandcsv" + "/" + url.split('/')[-3] + "/", url.split('/')[-2] + '.xlsx')
    Path(save_path + "/exclandcsv/" + "/" + url.split('/')[-3]).mkdir(parents=True, exist_ok=True)
    logging.info(f'Сохранение данных в файл Excel: {excel_path}')
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df_img = pd.DataFrame(img_src, columns=['Image path'])
        df_datasheet = pd.DataFrame([datasheet_src], columns=['Datasheet part'])
        df_file_3d = pd.DataFrame(file_3d_src, columns=['3d model part'])
        df_final = df.join(df_img, rsuffix='_datasheet')
        df_final = df_final.join(df_datasheet, rsuffix='_datasheet')
        df_final = df_final.join(df_file_3d, rsuffix='_datasheet')
        df_final.to_excel(writer, index=False, sheet_name=url.split('/')[-2])
        worksheet = writer.sheets[url.split('/')[-2]]
        worksheet.autofit()

def save_to_csv(df, img_src,datasheet_src, file_3d_src, save_path, url):
    # Удаляем столбец "Buy Now" если он существует
    if 'Buy Now' in df.columns:
        df = df.drop(columns=['Buy Now'])
    if(url.split('/')[-3] != "en"):
        csv_path = os.path.join(save_path + "/exclandcsv" + "/" + url.split('/')[-3] + "/", url.split('/')[-2] + '.csv')
        Path(save_path + "/exclandcsv/" + "/" + url.split('/')[-3]).mkdir(parents=True, exist_ok=True)
    else:
        csv_path = os.path.join(save_path + "/exclandcsv" + "/" + url.split('/')[-2] + "/", url.split('/')[-2] + '.csv')
        Path(save_path + "/exclandcsv/" + "/" + url.split('/')[-2]).mkdir(parents=True, exist_ok=True)

    logging.info(f'Сохранение данных в файл CSV: {csv_path}')
    df_img = pd.DataFrame(img_src, columns=['Image path'])
    try:
        df_datasheet = pd.DataFrame(datasheet_src, columns=['Datasheet part'])
    except:
        df_datasheet = pd.DataFrame(datasheet_src)
        logging.error("Не получилось получить расположение даташитов в один столбец")
    try:
        df_file_3d = pd.DataFrame(file_3d_src, columns=['3d model part'])
    except:
        df_file_3d = pd.DataFrame(file_3d_src)
        logging.error("Не получилось получить расположение 3д моделей в один столбец")
    df_final = df.join(df_img, rsuffix='_datasheet')
    df_final = df_final.join(df_datasheet, rsuffix='_datasheet')
    df_final = df_final.join(df_file_3d, rsuffix='_datasheet')
    try:
        df_final.columns = [(col.split('▲▼')[0]) for col in df_final.columns]
    except:
        df_final.columns = df_final.columns
        logging.error("Не получилось сделать красивые строки")
    df_final.to_csv(csv_path, index=False, sep=';')

async def main():
    print("Какие категории вы хотите пропарсить?\ndiodes - Диоды\nthyristors - Тиристоры\npower-ics - Силовые микросхемы\nanalog-switches - Аналоговый переключатели\nmosfets - Металл–оксид–полупроводник\noptocouplers - Оптосоединители\nrelays - реле\nreceiver - Приемники\nleds - Светильники\nphoto-detectors - Фото-детектеры\nir-em\ndisplays - Дисплеи\nmodules - модульные\ncapacitors - Конденсаторы\nresistors - Резисторы\n")
    inputer = input()
    with open('pages.json', 'r') as f:
        pages = json.load(f)
    if inputer == 'all':
        for pa in pages.keys():
            sl_use.append(pages[pa])
        print(sl_use)
    else:
        for use_in in inputer.split(','):
            if use_in in pages:
                print(f"Parsing category: {use_in}")
                for pa in pages[use_in]:
                    sl_use.append(pa)
            else:
                print(f"Category {use_in} not found in pages.json")
        print(sl_use)
    if inputer == 'all':
        for sl1 in sl_use:
            for sl in sl1:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60), headers=headers) as session:
                    with ThreadPoolExecutor(max_workers=4) as executor:
                        loop = asyncio.get_event_loop()
                        tasks = []
                        print(sl)
                        web_source = await loop.run_in_executor(executor, get_web, url + sl, sl)
                        df, img_src, datasheet_src = await process_html(session, web_source, sl)
                        file_3d_src = []
                        for fl in datasheet_src:

                            print(fl[:-3])
                        #print(os.path.exists("Datasheet\\"+fl[:-3]+"zip"))
                            if os.path.exists(fl[:-3] + "zip"):
                                file_3d_src.append(fl[:-3] + "zip")
                            else:
                                file_3d_src.append("None")

                    #save_to_excel(df, img_src, datasheet_src, file_3d_src,save_path, url + sl)
                        save_to_csv(df, img_src,datasheet_src, file_3d_src, save_path, url + sl)
                        logging.info('Данные успешно сохранены.')

                    await asyncio.gather(*tasks)
    else:
        for sl in sl_use:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60), headers=headers) as session:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    loop = asyncio.get_event_loop()
                    tasks = []
                    print(sl)
                    web_source = await loop.run_in_executor(executor, get_web, url + sl, sl)
                    df, img_src, datasheet_src = await process_html(session, web_source, sl)
                    file_3d_src = []
                    for fl in datasheet_src:
                        # print(fl[:-3])
                        # print(os.path.exists("Datasheet\\"+fl[:-3]+"zip"))
                        if os.path.exists(fl[:-3] + "zip"):
                            file_3d_src.append(fl[:-3] + "zip")
                        else:
                            file_3d_src.append("None")
                    # save_to_excel(df, img_src, datasheet_src, file_3d_src,save_path, url + sl)
                    save_to_csv(df, img_src, datasheet_src, file_3d_src, save_path, url + sl)
                    logging.info('Данные успешно сохранены.')

                await asyncio.gather(*tasks)
try:

    asyncio.run(main())
finally:
    driver.quit()
    if failed_downloads:
        with open("failed_downloads.txt", "w") as f:
            for url in failed_downloads:
                f.write(url + "\n")
    print("Всё")
