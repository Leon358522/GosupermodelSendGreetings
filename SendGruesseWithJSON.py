import re
import argparse
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as EdgeService
from typing import Any

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

DRIVER = webdriver.Chrome(options=options)
TIMER = 0.25
PAUSE = 0.4



with open('credentials.json') as f:
    credentials = json.load(f)


parser = argparse.ArgumentParser(prog='SendGreetings',
                                 description='Determine which credentials from the JSON file to use and determines to which model the greetings are send to',
                                 epilog='Make sure you have the credentials.json file in the same directory as this script')
parser.add_argument('-c',
                    "--credential_index",
                    metavar='N',
                    type=int,
                    nargs='+',
                    help='The indices of the credentials to use'
                    )
parser.add_argument('-t',
                    "--to_model",
                    choices=range(0, len(credentials), 1),
                    metavar='N',
                    type=int,
                    help='The indices of the models to send the greetings to',
                    )
args = parser.parse_args()


def select_model(model: str) -> Any:
    elem_hover = DRIVER.find_element(By.CSS_SELECTOR, f"a[Modelname={model}]")
    return elem_hover


def open_friend_page() -> None:
    ActionChains(DRIVER).move_to_element(DRIVER.find_element(By.CSS_SELECTOR))


def actions_click_and_perform(selector: Any) -> None:
    global PAUSE
    ActionChains(DRIVER).click(selector).pause(PAUSE).perform()


def send_greeting(yeahboy: Any, amount: int, best_friend: bool = False) -> None:
    wait = WebDriverWait(DRIVER, 3, 500)
    actions = ActionChains(DRIVER)
    DRIVER.execute_script("arguments[0].scrollIntoView();", yeahboy)
    global PAUSE
    actions.move_to_element(yeahboy).pause(PAUSE)
    actions.perform()
    selectors = [
                 "div[class=modeldialog_buttons] a[title*=Be]",
                 "#friend_badge_hug_table > tbody > tr:nth-child(4) > td > input",
                 "#friend_badge_hug_table > tbody > tr:nth-child(1) > td > input",
                 "#assign_button",
                 "#msgbox_ok",
                 "table[style='width\:460px'] tr "
                 ]

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selectors[0])))
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selectors[0])))
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors[0])))
    actions_click_and_perform(DRIVER.find_element(By.CSS_SELECTOR,
                                                  selectors[0]))  # Select Send Greeting
    if amount == 50 :
        options = DRIVER.find_elements(By.CSS_SELECTOR, selectors[5])
        pattern = re.compile(".+\d+.+")
        for option in options:
            # print(option.text, pattern.match(option.text), re.match(pattern, option.text))
            if pattern.match(option.text):
                actions_click_and_perform(option.find_element(By.CSS_SELECTOR,'input'))
    else:
        wait.until(EC.presence_of_element_located( (    By.CSS_SELECTOR, selectors[2])))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selectors[2])))
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectors[2])))
        
        actions_click_and_perform(DRIVER.find_element(By.CSS_SELECTOR,
                                                      selectors[2]))  # Select 1 G
    wait.until(EC.presence_of_element_located(
        (
        By.CSS_SELECTOR, selectors[3]))
        )
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selectors[3])))
    actions_click_and_perform(DRIVER.find_element(By.CSS_SELECTOR,
                                                  selectors[3]))  # Send
    # time.sleep(TIMER)
    wait.until(EC.presence_of_element_located(( By.CSS_SELECTOR, selectors[4])
    )
    )
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selectors[4])))
    actions.pause(PAUSE).move_to_element(DRIVER.find_element(By.CSS_SELECTOR, selectors[4])).click(DRIVER.find_element(By.CSS_SELECTOR, selectors[4]))
    actions.perform()
        # DRIVER.find_element(By.CSS_SELECTOR,
    #                     "span[onkeypress='var key=window.event?event.keyCode:event.which;if(key==13||key==32)closeMsgBox();return false;']").click()


def login(json_nummber: str) -> None:
    username_field = DRIVER.find_element(By.XPATH, "//input[@name='username']")
    username_field.send_keys(credentials[str(json_nummber)][0])
    pw_field = DRIVER.find_element(By.XPATH, "//input[@name='password']")
    pw_field.send_keys(credentials[str(json_nummber)][1])
    pw_field.send_keys(Keys.ENTER)


def use_girl(json_nummber: str, to_model: int) -> None:

    # DRIVER.implicitly_wait(5)
    DRIVER.get('https://gosupermodel.com')
    DRIVER.execute_script(script="window.scrollTo(0,0)")
    login(json_nummber)
    DRIVER.execute_script(script="window.scrollTo(0,0)")
    try:
        DRIVER.find_element(By.XPATH,
                            "//div[@id='pinball_frame']/div[7]").click()
    except Exception:
        pass
    DRIVER.find_element(By.XPATH,
                        "//div[@id='framework_all']/div/div[2]/div[2]/a[4]/div").click()
    DRIVER.execute_script(script="window.scrollTo(0,1000)")
    g_buttons = select_model(credentials[str(to_model)][0])
  #  greetings_started = int(DRIVER.find_element(By.CSS_SELECTOR, "#hugs").text)
  #  switched = False 
    name = credentials[str(to_model)][0]
    while True:
        ActionChains(DRIVER).move_to_element(DRIVER.find_element(By.CSS_SELECTOR,"#hugs")).perform()
        greetings = int(DRIVER.find_element(By.CSS_SELECTOR, "#hugs").text)
        g_buttons = select_model(credentials[str(to_model)][0])
        #experimentell
        # if json_nummber == 1 and greetings_started-greetings >= greetings_started/2 and switched != True:
        #     if list(credentials.keys()).index(str(to_model)) == 0:
        #         g_buttons = select_model(credentials[str(2)][0])
        #         name = credentials[str(2)][0]
        #     else:
        #         g_buttons = select_model(credentials[str(1)][0])
        #         name = credentials[str(1)][0]
        #     switched = True
        if (greetings >= 50):
            send_greeting(g_buttons, 50)
            print(
                f"Send 50 Greetings to {name}, {greetings-50} Grueße to go :D")
            continue
        elif (greetings >= 50 and json_nummber in [2, 3]):
            send_greeting(g_buttons, 50, True)
            print(
                f"Send 50 Greetings to {name}, {greetings-50} Grueße to go :D")
            continue
        elif (greetings > 0):
            send_greeting(g_buttons, 1)
            print(f"Send 1 greeting {name}, {greetings-1} Grueße to go :D")
            continue
        break
    DRIVER.find_element(By.XPATH, "//a[contains(text(),'Log out')]").click()


if __name__ == '__main__':
    DRIVER.implicitly_wait(3)
    for i in args.credential_index:
        use_girl(i, args.to_model)
    DRIVER.close()
