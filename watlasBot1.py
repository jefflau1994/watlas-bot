from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
from os import environ

USERNAME = environ['USERNAME']
PASSWORD = environ['PASSWORD']

chrome_options = Options()
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=1')

def bot1():
    
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('http://watlas.fantasyarea.com/watlas/index.cgi')
    wait = WebDriverWait(browser, 10)

    #登入
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/center/form/input[1]")))
    except:
        browser.quit()
        return
    element.send_keys(USERNAME)
    element = browser.find_element_by_xpath('/html/body/center/form/input[2]')
    element.send_keys(PASSWORD)
    element = browser.find_element_by_xpath('/html/body/center/form/input[4]')
    element.click()
    
    #讀取庫存 & 時間
    browser.get('http://watlas.fantasyarea.com/watlas/action.cgi')
    
    breadCount = int(wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table[3]/tbody/tr[2]/td[6]'))).text[:-1])
    wineCount = int(browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr[3]/td[6]').text[:-1])
    eggCount = int(browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr[4]/td[6]').text[:-1])
    ship1count = int(browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr[5]/td[6]').text[:-1])
    stamina = browser.find_element_by_xpath("/html/body/center/form/table/tbody/tr[1]/td[4]/table/tbody/tr[3]/td[2]").text
    
    if ("分" in stamina):
        stamina = stamina.replace("分",'')
        if ("小時" in stamina):
            hour, minute = stamina.split("小時")
        else:
            hour = 0
            minute = stamina
    else:
        minute = 0
        hour = stamina.replace("小時",'')
    
    hour = float(hour)
    minute = float(minute)/60
    gameTime = hour + minute

    #補充庫存(麵包 & 酒 & 蛋 & 船)
    if breadCount == 0:
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=buy&buy=0!0!18&bk=m!&')
        element = browser.find_element_by_xpath('/html/body/center/form/input[7]')
        element.send_keys("1000")
        element = browser.find_element_by_xpath('/html/body/center/form/input[8]')
        element.click()
        gameTime -=0.217

    if wineCount == 0:
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=buy&buy=0!1!19&bk=m!&')
        element = browser.find_element_by_xpath('/html/body/center/form/input[7]')
        element.send_keys("500")
        element = browser.find_element_by_xpath('/html/body/center/form/input[8]')
        element.click()
        gameTime -=0.217

    if eggCount == 0:
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=buy&buy=0!9!90&bk=m!&')
        element = browser.find_element_by_xpath('/html/body/center/form/input[7]')
        element.send_keys("1600")
        element = browser.find_element_by_xpath('/html/body/center/form/input[8]')
        element.click()
        gameTime -=0.217

    if (ship1count == 0 and gameTime > 33.8): 
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=buy&buy=0!3!15&bk=m!&')
        element = browser.find_element_by_xpath('/html/body/center/form/input[7]')
        element.send_keys("50")
        element = browser.find_element_by_xpath('/html/body/center/form/input[8]')
        element.click()
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=buy&buy=0!4!16&bk=m!&')
        element = browser.find_element_by_xpath('/html/body/center/form/input[7]')
        element.send_keys("50")
        element = browser.find_element_by_xpath('/html/body/center/form/input[8]')
        element.click()
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=item-m&item=1&no=0&&bk=s')
        element = browser.find_element_by_xpath('/html/body/center/form/input[5]')
        element.send_keys("50")
        element = browser.find_element_by_xpath('/html/body/center/form/input[6]')
        element.click()
        gameTime -=33.8

    #打掃
    browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=sweep')
    rubbish_text = browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr/td[2]').text
    num = re.findall(r"\d+", rubbish_text)[1]
    if (int(num) > 1 and num and gameTime > (int(num)-1)):
        element = browser.find_element_by_xpath('/html/body/center/form/input[2]')
        element.send_keys(str(int(num)-1))
        element = browser.find_element_by_xpath('/html/body/center/form/input[3]')
        element.click()
        gameTime -= (int(num)-1)
    
    #print to console
    localtime = time.asctime(time.localtime(time.time())) 
    print(localtime)
    print("bread:" + str(breadCount))
    print("wine:" + str(wineCount))
    print("egg:" + str(eggCount))
    print("ship1:" + str(ship1count))
    print(str(gameTime))
    
    #記錄庫存到txt      
    record = [localtime, "\t", str(breadCount), "\t", str(wineCount), "\t", str(eggCount), "\t", str(ship1count), "\n"]
    file1 = open("watlasRecord.txt", "a+")
    file1.writelines(record)
    file1.close()
    
    
    browser.quit()

while (1):
    bot1()
    time.sleep(900)



