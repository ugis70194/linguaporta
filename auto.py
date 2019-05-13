import selenium
from selenium import webdriver
from collections import OrderedDict
import time
import json

CHROME_PATH = './driver/chromedriver'
LUNGUAPORTA_URL = 'https://w5.linguaporta.jp/user/seibido/'
DELAY_sec = 0.3

def getUserData() :
    userData = json.load(open('user_data.json'))
    return userData

def saveUserData(userData) :
    userDataFile = open('user_data.json', mode='w')
    json.dump(userData, userDataFile, indent=4)
    userDataFile.close()

def getDriver() :
    driver = webdriver.Chrome(CHROME_PATH)
    return driver

def openBrowser(driver) :
   driver.get(LUNGUAPORTA_URL)
   time.sleep(DELAY_sec)

def inputId(driver, userData) :
    idInputFrom = driver.find_element_by_name('id')
    idInputFrom.send_keys(userData['id'])
    time.sleep(DELAY_sec)

def inputPass(driver, userData) :
    passInputFrom = driver.find_element_by_name('password')
    passInputFrom.send_keys(userData['pass'])
    time.sleep(DELAY_sec)

def clickLoginButton(driver) :
    loginButton = driver.find_element_by_id('btn-login')
    loginButton.click()
    time.sleep(DELAY_sec)

def toStudyPage(driver) :
    studyPageLink = driver.find_element_by_class_name('menu-study')
    studyPageLink.click()
    time.sleep(DELAY_sec)

def toUnitList(driver) :
    unitListButton = driver.find_element_by_class_name('btn-reference-select')
    unitListButton.click()
    time.sleep(DELAY_sec)

def toLearning(driver, index) :
    try : 
        learningButton = driver.find_element_by_xpath(
            "/html/body/div[@id='content']/div[@id='content-inner']/div[@id='content-study']/div[@class='table-resp table-unit-list']/div[@class='table-resp-row']["+str(index)+"]/div[@class='table-resp-col col-unitname']/div[@class='col-study']/input[@class='btn btn-study']"
        )
        learningButton.click()
        time.sleep(DELAY_sec)
        time.sleep(DELAY_sec)
        return False
    except selenium.common.exceptions.NoSuchElementException : 
        return True

def submitAnser(driver) :
    done = False
    while not done : 
        try : 
            time.sleep(DELAY_sec)
            ans = driver.find_element_by_id('answer_0_0')
            time.sleep(DELAY_sec)
            ans.click()
            time.sleep(DELAY_sec)

            submitButton = driver.find_element_by_id('ans_submit')
            time.sleep(DELAY_sec)
            submitButton.click()
            time.sleep(DELAY_sec + 0.6)
            toNext = driver.find_element_by_class_name('btn-problem-next')
            time.sleep(DELAY_sec)
            toNext.click()
            time.sleep(DELAY_sec + 0.4)
        except selenium.common.exceptions.NoSuchElementException : 
            returnToList = driver.find_element_by_class_name('btn-return-units')
            time.sleep(DELAY_sec)
            returnToList.click()
            done = True
            time.sleep(DELAY_sec + 0.3)
            return

def toNextPage(driver, nextPage) :
    if(nextPage > 20) :
        nextPage = nextPage % 20 +1
    toNextPageButton = driver.find_element_by_xpath(
        "/html/body/div[@id='content']/div[@id='content-inner']/div[@id='content-study']/div[@class='pagination unit_list_page']/a[@class='btn btn-page']["+str(nextPage)+"]"
    )
    toNextPageButton.click()
    time.sleep(DELAY_sec + 0.5)


def main():

    driver = getDriver()
    userData = getUserData()

    openBrowser(driver)
    inputId(driver, userData)
    inputPass(driver,userData)
    clickLoginButton(driver)

    toStudyPage(driver)
    toUnitList(driver)

    now = 1
    while now < userData['page'] :
        toNextPage(driver, now)
        now += 1

    indexes = None
    allDone = False
    while not allDone :
        thisPageDone = 0

        if now % 2 == 1:
            indexes = [1, 5, 11]
        else : 
            indexes = [3, 7, 11]

        if userData['page'] == 42 :
            allDone = True
            indexes = [3]

        for index in indexes :
            print(userData['page'], end="")
            print(" " + str(index))
            
            thisSessionDone = toLearning(driver, index)
            thisPageDone += thisSessionDone

            if not thisSessionDone:  
                submitAnser(driver)
            elif thisSessionDone and thisPageDone > 2:
                toNextPage(driver,now)
                userData['page'] += 1
                now += 1
                saveUserData(userData)

    driver.close()

if __name__ == '__main__':
    main()




