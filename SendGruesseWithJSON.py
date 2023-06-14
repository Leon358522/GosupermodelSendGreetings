import time
import argparse
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from typing import Any

EDGE_DRIVER = './edgedriver_win64/msedgedriver'
DRIVER = webdriver.Edge(EDGE_DRIVER)
TIMER = 0.25

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
                    choices=range(0, len(credentials["accounts"]), 1),
                    metavar='N',
                    type=int,
                    help='The indices of the models to send the greetings to',
                    )
args = parser.parse_args()


def select_model(model: str) -> Any:
    elem_hover = DRIVER.find_element_by_id(model)
    return elem_hover


def open_friend_page() -> None:
    action = ActionChains(DRIVER)
    action.move_to_element(DRIVER.find_element_by_css_selector())


def actions_click_and_perform(selector: Any) -> None:
    actions = ActionChains(DRIVER)
    actions.click(selector)
    actions.perform()


def send_greeting(yeahboy: Any, amount: int, best_friend: bool = False) -> None:
    actions = ActionChains(DRIVER)
    time.sleep(TIMER)
    actions.move_to_element(yeahboy)
    actions.perform()
    time.sleep(TIMER)
    actions_click_and_perform(DRIVER.find_element_by_css_selector(
        '.button:nth-child(11) > span'))  # Select Send Greeting
    time.sleep(TIMER)
    if amount == 50 and best_friend == True:
        actions_click_and_perform(DRIVER.find_element_by_css_selector(
            "tr:nth-child(4) input"))  # Select 50 G
    elif amount == 50 and best_friend != True:
        actions_click_and_perform(DRIVER.find_element_by_css_selector(
            "tr:nth-child(2) input"))  # Select 50 G
    else:
        actions_click_and_perform(DRIVER.find_element_by_css_selector(
            "tr:nth-child(1) input"))  # Select 1 G
    time.sleep(TIMER)
    actions_click_and_perform(DRIVER.find_element_by_css_selector(
        "#assign_button > span"))  # Send
    time.sleep(TIMER)
    DRIVER.find_element_by_css_selector(
        "span[onkeypress='var key=window.event?event.keyCode:event.which;if(key==13||key==32)closeMsgBox();return false;']").click()


def login(json_nummber: str) -> None:
    username_field = DRIVER.find_element_by_xpath("//input[@name='username']")
    username_field.send_keys(credentials[str(json_nummber)][0])
    pw_field = DRIVER.find_element_by_xpath("//input[@name='password']")
    pw_field.send_keys(credentials[str(json_nummber)][1])
    pw_field.send_keys(Keys.ENTER)


def use_girl(json_nummber: str, to_model: int) -> None:

    DRIVER.get('https://gosupermodel.com')
    DRIVER.execute_script(script="window.scrollTo(0,0)")
    DRIVER.implicitly_wait(5)
    login(json_nummber)
    DRIVER.execute_script(script="window.scrollTo(0,0)")
    try:
        DRIVER.find_element_by_xpath(
            "//div[@id='pinball_frame']/div[7]").click()
    except Exception:
        pass
    DRIVER.find_element_by_xpath(
        "//div[@id='framework_all']/div/div[2]/div[2]/a[4]/div").click()
    DRIVER.execute_script(script="window.scrollTo(0,1000)")
    g_buttons = select_model(credentials["accounts"][to_model])
    greetings_started = int(DRIVER.find_element_by_css_selector("#hugs").text)
    switched, name = False, credentials["accounts"][to_model]
    while True:
        greetings = int(DRIVER.find_element_by_css_selector("#hugs").text)
        if json_nummber == 1 and greetings_started-greetings >= greetings_started/2 and switched != True:
            if credentials["accounts"].index(credentials["accounts"][to_model]) == 0:
                g_buttons = select_model(credentials["accounts"][1])
                name = credentials["accounts"][1]
            else:
                g_buttons = select_model(credentials["accounts"][0])
                name = credentials["accounts"][0]
            switched = True
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
    DRIVER.find_element_by_xpath("//a[contains(text(),'Log out')]").click()


if __name__ == '__main__':
    for i in args.credential_index:
        use_girl(i, args.to_model)
    DRIVER.close()
