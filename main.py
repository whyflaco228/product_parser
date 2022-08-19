import requests
from bs4 import BeautifulSoup
import json
import csv

# URL = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
#
# req = requests.get(URL, headers=headers)
# src = req.text

# with open('index.html', 'r', encoding='utf-8-sig') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
#
# allProductsHrefs = soup.find_all(class_='mzr-tc-group-item-href')
#
# allCategoriesDict = {}
#
# for item in allProductsHrefs:
#     itemText = item.text
#     itemLink = 'https://health-diet.ru' + item.get('href')
#     allCategoriesDict[itemText] = itemLink
#
# with open('all_categories_dict.json', 'w', encoding='utf-8-sig') as file:
#     json.dump(allCategoriesDict, file, indent=4, ensure_ascii=False)
#
with open('all_categories_dict.json', 'r', encoding='utf-8-sig') as file:
    allCategories = json.load(file)

iterationCount = int(len(allCategories)) - 1
count = 0

print(f'Всего итераций: {iterationCount}')
for categoryName, categoryLink in allCategories.items():

    rep = [',', ' ', '-', '`']
    for item in rep:
        if item in categoryName:
            categoryName = categoryName.replace(item, '_')

    req = requests.get(url=categoryLink, headers=headers)
    src = req.text
    with open(f'data/{count}{categoryName}.html', 'w', encoding='utf-8-sig') as file:
        file.write(src)

    with open(f'data/{count}{categoryName}.html', 'r', encoding='utf-8-sig') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # alert
    alert = soup.find(class_='uk-alert-danger')
    if alert is not None:
        continue

    # сбор таблицы

    tableHead = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    print(tableHead)
    # извлечение из таблицы
    product = tableHead[0].text
    colories = tableHead[1].text
    proteins = tableHead[2].text
    fats = tableHead[3].text
    carbohydrates = tableHead[4].text

    with open(f'data/{count}_{categoryName}.csv', 'w', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                product,
                colories,
                proteins,
                fats,
                carbohydrates
            )
        )

        # сбор данных продуктов

        productsData = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
        for item in productsData:
            productTds = item.find_all('td')
            product = productTds[0].find('a').text
            colories = productTds[1].text
            proteins = productTds[2].text
            fats = productTds[3].text
            carbohydrates = productTds[4].text
            with open(f'data/{count}_{categoryName}.csv', 'a', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    (
                        product,
                        colories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )
    count += 1
    print(f'Итерация: {count}. {categoryName} записан...')
    iterationCount = iterationCount - 1
    if iterationCount == 0:
        print('Работа закончена')
        break
    print(f'Осталось итераций: {iterationCount}')
