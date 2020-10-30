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
        print("登入失敗")
        return
    element.send_keys(USERNAME)
    element = browser.find_element_by_xpath('/html/body/center/form/input[2]')
    element.send_keys(PASSWORD)
    element = browser.find_element_by_xpath('/html/body/center/form/input[4]')
    element.click()
    
    #讀取 庫存&遊戲時間
    browser.get('http://watlas.fantasyarea.com/watlas/action.cgi')
    
    breadCount = int(wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/center/table[3]/tbody/tr[2]/td[6]'))).text[:-1])
    wineCount = int(browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr[3]/td[6]').text[:-1])
    eggCount = int(browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr[4]/td[6]').text[:-1])
    ship1count = int(browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr[5]/td[6]').text[:-1])
    ship2count = int(browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr[6]/td[6]').text[:-1])
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
    
    
    
    #行動 補充庫存 (包 & 酒 & 蛋 & 船)
    if breadCount == 0:
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=buy&buy=0!0!18&bk=m!&')
        element = browser.find_element_by_xpath('/html/body/center/form/input[7]')
        element.send_keys("1000")
        element = browser.find_element_by_xpath('/html/body/center/form/input[8]')
        element.click()
        gameTime -=0.217
        print("已買包")

    if wineCount == 0:
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=buy&buy=0!1!19&bk=m!&')
        element = browser.find_element_by_xpath('/html/body/center/form/input[7]')
        element.send_keys("500")
        element = browser.find_element_by_xpath('/html/body/center/form/input[8]')
        element.click()
        gameTime -=0.217
        print("已買酒")

    if eggCount == 0:
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=buy&buy=0!9!90&bk=m!&')
        element = browser.find_element_by_xpath('/html/body/center/form/input[7]')
        element.send_keys("1600")
        element = browser.find_element_by_xpath('/html/body/center/form/input[8]')
        element.click()
        gameTime -=0.217
        print("已買蛋")

    if (ship1count == 0 and gameTime > 11.3): 
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
        gameTime -=11.3
        print("已造船1")

    if (ship2count == 0 and gameTime > 8.77): 
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=buy&buy=0!3!15&bk=m!&')
        element = browser.find_element_by_xpath('/html/body/center/form/input[7]')
        element.send_keys("25")
        element = browser.find_element_by_xpath('/html/body/center/form/input[8]')
        element.click()
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=buy&buy=0!4!16&bk=m!&')
        element = browser.find_element_by_xpath('/html/body/center/form/input[7]')
        element.send_keys("25")
        element = browser.find_element_by_xpath('/html/body/center/form/input[8]')
        element.click()
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=item-m&item=1&no=1&&bk=s')
        element = browser.find_element_by_xpath('/html/body/center/form/input[5]')
        element.send_keys("25")
        element = browser.find_element_by_xpath('/html/body/center/form/input[6]')
        element.click()
        gameTime -=8.77
        print("已造船2")

    #行動 買賣種子
    browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=manor')
    seed1count = int(browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr[2]/td[4]').text[0])
    seed2count = int(browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr[3]/td[4]').text[0])
    seed3count = int(browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr[4]/td[4]').text[0])
    if browser.find_elements_by_xpath("/html/body/center/form/input[3]"):
        element = browser.find_element_by_xpath("/html/body/center/form/input[3]")
        element.click()
        print("已賣種子")
    if seed1count == 0:
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=manor-m&&buy=0&bk=manor')
        element = browser.find_element_by_xpath('/html/body/center/form/input[4]')
        element.send_keys("20")
        element = browser.find_element_by_xpath('/html/body/center/form/input[5]')
        element.click()
        print("已買種子1")
    if seed2count == 0:
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=manor-m&&buy=1&bk=manor')
        element = browser.find_element_by_xpath('/html/body/center/form/input[4]')
        element.send_keys("20")
        element = browser.find_element_by_xpath('/html/body/center/form/input[5]')
        element.click()
        print("已買種子2")
    if seed3count == 0:
        browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=manor-m&&buy=2&bk=manor')
        element = browser.find_element_by_xpath('/html/body/center/form/input[4]')
        element.send_keys("20")
        element = browser.find_element_by_xpath('/html/body/center/form/input[5]')
        element.click()
        print("已買種子3")

    #行動 打掃
    browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=sweep')
    rubbish_text = browser.find_element_by_xpath('/html/body/center/table[3]/tbody/tr/td[2]').text
    if (re.findall(r"\d+", rubbish_text) == []):
        num = "0"
        rubbish = "0"
    else:
        num = re.findall(r"\d+", rubbish_text)[1]
        rubbish = re.findall(r"\d+", rubbish_text)[0]
    
    if (int(num) > 1 and gameTime > (int(num)-1)):
        element = browser.find_element_by_xpath('/html/body/center/form/input[2]')
        element.send_keys(str(int(num)-1))
        element = browser.find_element_by_xpath('/html/body/center/form/input[3]')
        element.click()
        gameTime -= (int(num)-1)
        print("已打掃")

    #行動 買狗
    browser.get('http://watlas.fantasyarea.com/watlas/action.cgi?key=shop-m')
    element = browser.find_elements_by_partial_link_text("看門狗")
    if element:
        browser.find_element_by_partial_link_text("看門狗").click()
        if browser.find_elements_by_xpath('/html/body/center/form/input[7]'):
            browser.find_element_by_xpath('/html/body/center/form/input[7]').send_keys("1")
            browser.find_element_by_xpath('/html/body/center/form/input[8]').click()
            print("已買看門狗")
            
    #行動 Print to console
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(localtime+"\t包:"+str(breadCount)+"\t酒:"+str(wineCount)+"\t蛋:"+str(eggCount)+"\t船1:"+str(ship1count)+"\t船2:"+str(ship2count)+"\t時間:"+str(int(gameTime))+"h\t垃圾:"+rubbish+"kg")
        
        
    #記錄庫存到txt      
    #record = [localtime, "\t", str(breadCount), "\t", str(wineCount), "\t", str(eggCount), "\t", str(ship1count), "\n"]
    #file1 = open("watlasRecord.txt", "a+")
    #file1.writelines(record)
    #file1.close()
    
    
    browser.quit()

while (1):
    bot1()
    time.sleep(900)
