from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
import time
import os
import re
import urllib.request
from multiprocessing import Pool

# 음식 이름 넣기, 최대 8개로 설정


def food_name_input():
    food_list = []
    count = 3
    while True:
        food_name = input(f"검색할 음식은?(남은개수 {count}개): ")
        if count == 0 or food_name == 'End':
            break

        food_list.append(food_name)
        count -= 1

    return food_list


# 이름별 폴더생성
def create_Folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def image_download(food):
    driver = webdriver.Chrome("C:/Users/sja95/chromedriver.exe")
    driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
    driver.maximize_window()
    elem = driver.find_element_by_name("q")
    create_Folder('./'+food+'')
    elem.send_keys(food)
    elem.send_keys(Keys.RETURN)

    SCROLL_PAUSE_TIME = 1

    last_height = driver.execute_script(
        "return document.body.scrollHeight")

    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script(
            "return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break
        last_height = new_height
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    count = 1
    # 테스트를 위해 각 키워드 당 이미지 10개로 한정
    for image in images[:100]:
        try:
            start = time.time()
            image.click()
            time.sleep(2)
            url = driver.find_element_by_xpath(
                '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img').get_attribute("src")
            urllib.request.urlretrieve(
                url, "./"+food+"/"+food+"_"+str(count)+".jpg")
            print(str(count)+'/'+str(100)+' '+food +
                  ' 다운로드 중...time : '+str(time.time() - start)[:5]+' 초')
            count += 1
        except:
            pass
    print(food+' ---다운로드 완료---')


# image_download(food_list)
# 4개 동시 실행이 안되서 수정필요
if __name__ == '__main__':
    pool = Pool()
    pool.map(image_download, food_name_input())