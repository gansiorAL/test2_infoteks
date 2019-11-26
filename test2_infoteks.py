# Модуль test2_InfoTeks, получает с сайта https://habr.com/ru/
# самые популярные посты за год.
# Входные данные: число count - количество получаемых постов
# Выходные данные: таблица , в каждой строке которой должны находиться:
# заголовок поста, короткое описание поста, дата публикации, имя автора поста

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import defaultdict
import re


def init_drive(brauser):
    """
    Инициализация драйвера
    :param brauser: Название браузеров GoogleChrome Firefox
    :return:
    """
    if brauser=="GoogleChrome":
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        full_path = os.path.abspath('chromedriver78_0_3904')
        driver = webdriver.Chrome(full_path,chrome_options=options)
    if brauser == "Firefox":
        print("Firefox not here.")
    return driver

def pages(driver,kol_t,start_page):
    """
    формируем необходимый массив страниц
    :param driver:
    :param kol_t:
    :param start_page:
    :return:
    """
    driver.get(start_page)
    name_ur=driver.find_elements(By.XPATH,'//div[@class="posts_list"]/ul/li/article/h2/a')
    ppages=[]
    ppages.append(start_page)
    if kol_t>len(name_ur):
        kol_pages=int(kol_t / len(name_ur))+1
        col_pages = driver.find_elements(By.XPATH,
                                         '//*[@class="toggle-menu__item toggle-menu__item_pagination"]/a')
        for ind_page in range(kol_pages-1):
            ppages.append(col_pages[ind_page].get_attribute("href"))
    return ppages

def get_content_page(kol_t, com_col, driver, is_page, mas_articals):
    """
    Пплучаем необходимое содержание со страницы
    :param kol_t: количество необходимых статей
    :param com_col: количество статей уже сформированных
    :param driver: драйвер
    :param is_page: начальная страница
    :param mas_articals: массив статей
    :return:
    """
    driver.get(is_page)
    #
    name_ur = driver.find_elements(By.XPATH,
                                   '//div[@class="posts_list"]/ul/li/article/h2/a')
    #
    short_text = driver.find_elements(By.XPATH,
                                      '//*[@class="post__text post__text-html js-mediator-article"]')
    #
    date_pub = driver.find_elements(By.XPATH, '//*[@class="post__time"]')
    #
    autor = driver.find_elements(By.XPATH,
                                 '//*[@class="user-info__nickname user-info__nickname_small"]')

    for i in range(len(name_ur)):
        if com_col<kol_t :
            com_col+=1
            ik=re.sub("^\s+|\n|\r|\s+$", '', name_ur[i].text)
            mas_articals[ik].append(re.sub("^\s+|\n|\r|\s+$", '',short_text[i].text))
            mas_articals[ik].append(re.sub("^\s+|\n|\r|\s+$", '',date_pub[i].text))
            mas_articals[ik].append(re.sub("^\s+|\n|\r|\s+$", '',autor[i].text))
        else:break

def print_table(mas_articals):
    """
    Печать таблицы
    :param mas_articals:
    :return:
    """
    pol = [30,80,23,20]
    print('='*sum(pol))
    print('{:^30} | {:^80} | {:^23} | {:^20}'.format('Название', 'Краткое содержание',
                           'Дата публикации','Автор'))
    print('-' * sum(pol))
    for kk in mas_articals:
        print('{:30} | {:80} | {:23} '
              '| {:20}'.format(kk[:pol[0]],mas_articals[kk][0][:pol[1]],mas_articals[kk][1],mas_articals[kk][2]))
        print('-'*sum(pol))
    print('=' * sum(pol))

def main_path(kol_t):
    """
    Основной модуль вывода контента
    :param kol_t: Количество необходимых статей
    :return:
    """
    driver = init_drive("GoogleChrome")
    start_page='https://habr.com/ru/top/yearly/'
    list_pages=pages(driver, kol_t, start_page) #определяем сколько страниц надо вывести
    mas_articals= defaultdict(list)             #определяем массив статей
    com_col=0

    for is_page in list_pages:                  #обрабатываем страницы
        get_content_page(kol_t, com_col, driver, is_page, mas_articals)
    print_table(mas_articals)


def trust_chislo(obras):
    """
    проверяем вводится ли числа
    :param obras: строка числа
    :return: False True
    """
    set_in=(['0','1','2','3','4','5','6','7','8','9'])
    resh=True
    for sim in obras:
        if sim not in set_in:
            resh=False
    return resh



if __name__=="__main__":
    print("Введите необходимое количество постов популярных в этом году. Выход q.")
    kol_t='e'
    while True :
        kol_t=input(" Kоличество постов(целое число):")
        if kol_t=='q':break
        else:
            if trust_chislo(kol_t):
                main_path(int(kol_t))
            else: continue