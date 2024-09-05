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



assignments = ['https://learn.zybooks.com/zybook/TAMUCSCE120-121-709Spring2023/chapter/11/section/7'           
               ]



for section in assignments:
    # need this or else will encounter error when trying to open multiple links
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors-spki-list")
    chrome_options.add_argument('--ignore-ssl-errors')

    s = Service(ChromeDriverManager().install()) # manages chromedriver
    driver = webdriver.Chrome(service=s, options=chrome_options)
    # Get website (STARTS LOGIN PAGE)
    driver.get(section)
    print('Opening', section,'...')
    print()
    # username
    userSearch = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Email')]")
    # userSearch = driver.find_element(By.ID, "ember9")
    userSearch.send_keys("") #tamu email here
    # password
    passSearch = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Password')]")
    # passSearch = driver.find_element(By.ID, "ember11")
    passSearch.send_keys("") # password here
    # ENTER
    passSearch.send_keys(Keys.RETURN)
    time.sleep(5) # wait for sign in


    # IN WEBSITE

    # ---- ANIMATIONS ----
    # check 2x boxes
    print('Starting Animations...')
    speedChecks = driver.find_elements(By.CLASS_NAME, "speed-control")
    totChecks = 0
    for check in speedChecks:
        check.click()
        button = driver.find_element(By.XPATH, '//button[normalize-space()="Start"]')
        #print('Clicking 2x check')
        print('.')
        button.click()
        totChecks += 1
        time.sleep(0.5)

    animationControl = driver.find_elements(By.CLASS_NAME, 'animation-controls')
    print("ANIMATION CONTROLS:", animationControl)
    animationDone = False
    #SCROLL TO TOP
    if len(animationControl) > 0:
        desired_y = (animationControl[0].size['height'] / 2) + animationControl[0].location['y']
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        #https://stackoverflow.com/questions/41744368/scrolling-to-element-using-webdriver
    else:
        animationDone = True

    done = 0
    ndx = 1
    # numActiveAnimations = len(animationControl)
    while animationDone == False:
        for i in range(len(animationControl)):
            print(". Scrolling to animation...")
            # scroll to button
            desired_y = (animationControl[i].size['height'] / 2) + animationControl[i].location['y']
            window_h = driver.execute_script('return window.innerHeight')
            window_y = driver.execute_script('return window.pageYOffset')
            current_y = (window_h / 2) + window_y
            scroll_y_by = desired_y - current_y
            driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
            time.sleep(1) # 1 sec grace period before checking
            # accesses button
            buttonStatus = animationControl[i].find_elements(By.XPATH, "//button[contains(@class, 'normalize-controls')]")
            
            # gets button status, play, pause, or play again
            x = buttonStatus[ndx]
            actions = ActionChains(driver)
            actions.move_to_element(x).perform()
            #print("     ndx:",ndx)
            aria_label = x.get_attribute("aria-label")
            print(". STATUS:", aria_label)
            if aria_label == 'Play again':
                print(". FINISHED ONE ANIMATION")
            elif aria_label == 'Play':
                print('. Playing...')
                x.click()
            time.sleep(0.5)
            ndx += 2

            # COUNT HOW MANY DONE
            finishedCounter = 0
            for j in buttonStatus:
                #print('--Attribute', j.get_attribute("aria-label"))
                if j.get_attribute("aria-label") == 'Play again':
                    finishedCounter += 1
            # IF DONE
            if finishedCounter == totChecks:
                animationDone = True
                break
            finishedCounter = 0
            #print("NUM ACTIVE:", numActiveAnimations)
        ndx = 1
    print('Finished animations...')
    time.sleep(1)
    print()

    # ---- FILL IN THE BLANKS ----
    print('Filling in the blanks...')
    print()

    showAnswerButton = driver.find_elements(By.XPATH, "//button[contains(@class, 'show-answer-button')]")
    for answer in showAnswerButton:
        print('.')
        # scroll to button
        desired_y = (answer.size['height'] / 2) + answer.location['y']
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        # double click
        answer.click()
        answer.click()

    answers = driver.find_elements(By.XPATH, "//span[contains(@class, 'forfeit-answer')]")
    textFields = driver.find_elements(By.XPATH, "//textarea[contains(@class, 'ember-text-area')]")
    checkButtons = driver.find_elements(By.XPATH, "//button[contains(@class, 'zb-button  primary  raised           check-button')]")
    for x in range(len(answers)):
        print('.')
        # retrieve answer and store
        finalAnswer = answers[x].text
        #print(finalAnswer)
        # insert answer into textbox
        textFields[x].send_keys(finalAnswer)
        # press CHECK
        checkButtons[x].click()


    print('Finished blanks!')
    print()

    # ---- MULTIPLE CHOICE ----
    print('Doing multiple choice...')
    questions = driver.find_elements(By.CLASS_NAME, 'question-choices')
    ##### DON'T NEED TO END ON CORRECT CUZ IT COUNTS RIGHT IF U CLICK IT ONCE ######
    # possibleCorrectCheckers = driver.find_elements(By.XPATH, ".//div[contains(@class, 'zb-explanation')]")
    # correctChecker = [] # list of mcq correct checkers
    # for candidate in possibleCorrectCheckers:
    #     rolePresence = candidate.get_attribute('role')
    #     if rolePresence != None: # only frqs have role attribute, so this will filter mcq's
    #         correctChecker.append(candidate)

    # print("number of correctCheckers for MCQ", len(correctChecker))
    ##############################

    for qndx in range(len(questions)):
        desired_y = (questions[qndx].size['height'] / 2) + questions[qndx].location['y']
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        
        answerChoices = questions[qndx].find_elements(By.XPATH, ".//div[contains(@class, 'zb-radio-button')]")
        for a in answerChoices:
            a.click()
            print('.')
            time.sleep(1)
        
    print('Finished multiple choices!')
    print()
    print('DONE WITH', section)
    print()

    # ---- DONE ----
    time.sleep(3)
    print('Closing website...')
    driver.quit()


