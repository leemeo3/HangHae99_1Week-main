import time
from selenium import webdriver

from flask import Flask
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.xevhlvh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# xpath 시작
# driver = webdriver.Chrome()
# driver.get('https://ediya.com/contents/drink.html?chked_val=12,&skeyword=#c');
# driver.get('https://ediya.com/contents/drink.html?chked_val=12,&skeyword=#c');

# driver = webdriver.Chrome('/Users/sanghoonlee/Desktop/sparta')
# driver.get('http://www.google.com/xhtml');
# time.sleep(5)
#
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5)
#
# driver.quit()
# m_morebox = driver.find_element_by_xpath('//*[@id="contentWrap"]/html/body/section/div[5]/div/div/a')
# m_morebox = driver.find_element_by_xpath('//*[@id="contentWrap"]/div[5]/div/div/a')
# m_morebox.click()
# time.sleep(1)

# driver = webdriver.Chrome('/Users/sanghoonlee/Desktop/sparta')
# driver.get('http://www.google.com/xhtml');
# time.sleep(5)
#
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5)
#
# driver.quit()
# xpath 종료

# 커피 시작
i = 0
data = requests.get('https://ediya.com/contents/drink.html?chked_val=12,&skeyword=#blockcate', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
coffees = soup.select('#menu_ul > li')
for coffee in coffees:
    i += 1
    name = coffee.select_one('div.menu_tt > a:nth-child(1) > span').text
    img = coffee.select_one('li > a > img')
    img_src = "https://ediya.com" + img.get("src")
    desc = coffee.select_one('div.pro_detail > div.detail_con > p').text
    calorie = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl > dd').text.replace("(","").replace(")","")
    sugar = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(2) > dd').text.replace("(","").replace(")","")
    protein = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(3) > dd').text.replace("(","").replace(")","")
    protein = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(3) > dd').text.replace(
        "(", "").replace(")", "")
    fat = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(4) > dd').text.replace(
        "(", "").replace(")", "")
    salt = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(5) > dd').text.replace(
        "(", "").replace(")", "")
    caffeine = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(6) > dd').text.replace(
        "(", "").replace(")", "")

    print(name)
    print(img_src)
    print("설명 : " + desc)
    print("칼로리 " + calorie)
    print("당류 " + sugar)
    print("단백질 " + protein)
    print("지방 " + fat)
    print("나트륨 " + salt)
    print("카페인 " + caffeine)
    print()

    doc = {
        "cafe": "ediya",
        "coffee_id": i,
        "coffee_name": name,
        "coffee_image": img_src,
        "coffee_desc": desc,
        "type": "coffee",
        "calorie": calorie,
        "salt": salt,
        "saturated_fat": fat,
        "sugars": sugar,
        "protein": protein,
        "caffeine": caffeine
    }
    db.coffee.insert_one(doc)
# 커피 종료

# 논 커피 시작
nn = 13 # 논커피 시작 번호
for j in range(0, 4):
    n = str(nn)
    print(n)
    result = 'https://ediya.com/contents/drink.html?chked_val=' + n + ',&skeyword=#blockcate'
    nn += 1
    data = requests.get(result, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    coffees = soup.select('#menu_ul > li')
    for coffee in coffees:
        i += 1
        name = coffee.select_one('div.menu_tt > a:nth-child(1) > span').text
        img = coffee.select_one('li > a > img')
        img_src = "https://ediya.com" + img.get("src")
        desc = coffee.select_one('div.pro_detail > div.detail_con > p').text
        calorie = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl > dd').text.replace("(","").replace(")","")
        sugar = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(2) > dd').text.replace("(","").replace(")", "")
        protein = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(3) > dd').text.replace("(", "").replace(")", "")
        protein = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(3) > dd').text.replace("(", "").replace(")", "")
        fat = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(4) > dd').text.replace("(", "").replace(")", "")
        salt = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(5) > dd').text.replace("(", "").replace(")", "")
        caffeine = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(6) > dd').text.replace("(", "").replace(")", "")

        print(name)
        print(i)
        print(img_src)
        print("설명 : " + desc)
        print("칼로리 " + calorie)
        print("당류 " + sugar)
        print("단백질 " + protein)
        print("지방 " + fat)
        print("나트륨 " + salt)
        print("카페인 " + caffeine)
        print()

    doc = {
        "coffee_id" : i,
        "cafe": "ediya",
        "coffee_name": name,
        "coffee_image": img_src,
        "coffee_desc": desc,
        "type": "non-coffee",
        "calorie": calorie,
        "salt": salt,
        "saturated_fat": fat,
        "sugars": sugar,
        "protein": protein,
        "caffeine": caffeine
    }
    db.coffee.insert_one(doc)
# 논 커피 종료

# 시즌 메뉴 시작
data = requests.get('https://ediya.com/contents/drink.html?chked_val=132,&skeyword=#blockcate', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
coffees = soup.select('#menu_ul > li')
for coffee in coffees:
    i += 1
    name = coffee.select_one('div.menu_tt > a:nth-child(1) > span').text
    img = coffee.select_one('li > a > img')
    img_src = "https://ediya.com" + img.get("src")
    desc = coffee.select_one('div.pro_detail > div.detail_con > p').text
    calorie = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl > dd').text.replace("(","").replace(")","")
    sugar = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(2) > dd').text.replace("(","").replace(")","")
    protein = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(3) > dd').text.replace("(","").replace(")","")
    protein = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(3) > dd').text.replace(
        "(", "").replace(")", "")
    fat = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(4) > dd').text.replace(
        "(", "").replace(")", "")
    salt = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(5) > dd').text.replace(
        "(", "").replace(")", "")
    caffeine = coffee.select_one('div.pro_detail > div.pro_comp > div.pro_nutri > dl:nth-child(6) > dd').text.replace(
        "(", "").replace(")", "")

    print(name)
    print(i)
    print(img_src)
    print("설명 : " + desc)
    print("칼로리 " + calorie)
    print("당류 " + sugar)
    print("단백질 " + protein)
    print("지방 " + fat)
    print("나트륨 " + salt)
    print("카페인 " + caffeine)
    print()

    doc = {
        "cafe": "ediya",
        "coffee_id": i,
        "coffee_name": name,
        "coffee_image": img_src,
        "coffee_desc": desc,
        "type": "non-coffee",
        "calorie": calorie,
        "salt": salt,
        "saturated_fat": fat,
        "sugars": sugar,
        "protein": protein,
        "caffeine": caffeine
    }
    db.coffee.insert_one(doc)
# 시즌 메뉴 종료
