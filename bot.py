import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import os.path
import time

# need this or else will encounter error when trying to open multiple links
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors-spki-list")
chrome_options.add_argument('--ignore-ssl-errors')

s = Service(ChromeDriverManager().install()) # manages chromedriver
driver = webdriver.Chrome(service=s, options=chrome_options)


# Get website (STARTS LOGIN PAGE)
driver.get("https://learn.zybooks.com/zybook/TAMUCSCE120-121-709Spring2023/chapter/8/section/3")
print('Opening', driver.title,'...')
print()
driver.maximize_window()
# username
userSearch = driver.find_element(By.ID, "ember9")
userSearch.send_keys("timwng@tamu.edu")
# password
passSearch = driver.find_element(By.ID, "ember11")
passSearch.send_keys("Kttw3972")
# ENTER
passSearch.send_keys(Keys.RETURN)
time.sleep(5) # wait for sign in


# IN WEBSITE
# check 2x boxes
print('Starting Animations...')
speedChecks = driver.find_elements(By.CLASS_NAME, "speed-control")
totChecks = 0
for check in speedChecks:
    check.click()
    button = driver.find_element(By.XPATH, '//button[normalize-space()="Start"]')
    print('Clicking 2x check')
    button.click()
    totChecks += 1
    time.sleep(1)

animationControl = driver.find_elements(By.CLASS_NAME, 'animation-controls')
print("ANIMATION CONTROLS:", animationControl)
#SCROLL TO TOP
desired_y = (animationControl[0].size['height'] / 2) + animationControl[0].location['y']
window_h = driver.execute_script('return window.innerHeight')
window_y = driver.execute_script('return window.pageYOffset')
current_y = (window_h / 2) + window_y
scroll_y_by = desired_y - current_y

print('scrolled to top!')
time.sleep(2)
done = 0
ndx = 1
numActiveAnimations = len(animationControl)
animationDone = False
while animationDone == False:
    for i in range(numActiveAnimations):
        print("Scrolling to animation...")
        # scroll to button
        desired_y = (animationControl[i].size['height'] / 2) + animationControl[i].location['y']
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        time.sleep(2) # 1 sec grace period before checking
        # accesses button
        buttonStatus = animationControl[i].find_elements(By.XPATH, "//button[contains(@class, 'normalize-controls')]")
        
        # gets button status, play, pause, or play again
        x = buttonStatus[ndx]
        actions = ActionChains(driver)
        actions.move_to_element(x).perform()
        print("     ndx:",ndx)
        aria_label = x.get_attribute("aria-label")
        print("STATUS:", aria_label)
        if aria_label == 'Play again':
            numActiveAnimations -= 1
            print("!!!!!!!!FINISHED ONE!!!!!!!!")
        elif aria_label == 'Play':
            print('Playing...')
            x.click()
        time.sleep(2)
        ndx += 2

        # COUNT HOW MANY DONE
        finishedCounter = 0
        for j in buttonStatus:
            print('--Attribute', j.get_attribute("aria-label"))
            if j.get_attribute("aria-label") == 'Play again':
                finishedCounter += 1
        # IF DONE
        if finishedCounter == totChecks:
            animationDone = True
            break
    
        print("NUM ACTIVE:", numActiveAnimations)


    ndx = 1
    time.sleep(1)
print('Finished animations...')
print()

print('Filling in the blanks...')
print()
        
        


totChecks = totChecks + 1
print()


# animations
# print('Starting animations...')
# animChecks = driver.find_elements(By.CLASS_NAME, "animation-controls")
# for a in animChecks:
#     #button = a.find_element(By.CLASS_NAME, "title")
#     button = a.find_element(By.XPATH, '//button[normalize-space()="Start"]')
#     print('Clicking', button.text)
#     #print("ID:", a.get_attribute("id"))
#     button.click()
# print()
# x = 0
# while x < totChecks:
#     if 

# fill in the blanks
#blanks = driver.find_elements(By.CLASS_NAME, "question-set-question short-answer-question ember-view")


# done
time.sleep(10)
print('Closing website...')
driver.quit()


