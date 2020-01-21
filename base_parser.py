import re
import urllib.request
from pprint import pprint

from bs4 import BeautifulSoup
from parser_src import prsr_source

BASE_URL = 'http://weblancer.net/jobs/'

# получение "сырой" html со страницы
def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

# пагинация по сайту (потому что парсинг происходит только на загруженой странице, а не по всех данных)
def get_page_count(html):
    soup = BeautifulSoup(markup=html, features="html.parser")   # определение объекта bs
    paggination = soup.find(name='div', class_='col-1 col-sm-2 text-right')
    last_page = 0
    for link in paggination.findAll('a'):
        number = link.get('href')
        last_page = re.search(r'\d+', number).group()

    return int(last_page)

# parsing
def parse(html):
    soup = BeautifulSoup(markup=html, features="html.parser")   # определение объекта bs
    table = soup.find(name='div', class_='cols_table')   # блок("таблица") откуда парсится нужная информация

    jobs = []

    for row in table.find_all_next(name='div', class_='row click_container-link set_href'):    # все записи("заявки") в таблице
        cols = row.find_all(name='div')
        categories = row.find_all(name='div', class_='text-muted')
        prices = row.find_all(name='div', class_='float-right float-sm-none title amount indent-xs-b0')
        applications = row.find_all(name='div', class_='float-left float-sm-none text_field')

        jobs.append({
            'title' : cols[0].a.text.strip(),
            'category' : categories[0].text.strip(),
            'price' : prices[0].text.strip(),
            'application' : applications[0].text.strip(),
        })
    return jobs




def main():
    page_count = get_page_count(get_html(BASE_URL))
    print("Всего страниц: %d" %page_count)

    jobs = []


    for page in range(1, page_count):
        print("Парсинг %d%%" %(page/page_count*100))
        jobs.extend(parse(get_html(BASE_URL + '?page=%d' %page)))

    for job in jobs:
        print(job)

if __name__ == '__main__':
    main()

