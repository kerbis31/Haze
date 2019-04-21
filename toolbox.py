from appium.webdriver import Remote
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from loguru import logger
from selenium import webdriver
import os
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

apk = os.path.join(os.environ['HOME'], 'Downloads', 'app-consumer-release.apk')

class Toolbox:
    ALL_BY_XPATH = '//*[not(*)]'
    # @property
    @staticmethod
    def nexar_appium_desired_capadibilties():
        return {
            'appActivity': '.architecture.activities.home.HomeActivity',
            'appPackage': 'mobi.nexar.dashcam',
            'platformVersion': 9,
            'deviceName': 'PIXEL 2 ',
            'platformName': 'Android',
            'app': os.path.join(os.environ['HOME'], 'Downloads', 'app-consumer-release.apk'),
            'noReset': True,
            'dontStopAppOnReset': True,
            'newCommandTimeout': 120

        }

    @staticmethod
    def chrome_appium_desired_capadibilties():
        return {
            'platformVersion': 9,
            'deviceName': 'PIXEL 2',
            'platformName': 'Android',
            'app': apk,
            'browserName' : "Chrome"
        }

    @staticmethod
    def sms_appium_desired_capabilities():
        return {
            'appActivity': '.ui.ConversationListActivity',
            'appPackage': 'com.google.android.apps.messaging',
            'platformVersion': 9,
            'deviceName': 'PIXEL 2',
            'platformName': 'Android',
            'app': apk,
            'autoGrantPermissions': True,
            'noReset': True
        }

    @staticmethod
    def binary_path():
        return os.path.join(os.environ['HOME'], 'Downloads', 'chromedriver')



    def driver(self, which='Nexar') -> Remote:
        if 'chrome' in which:
            return webdriver.Chrome(executable_path=self.binary_path())
        elif 'Appium_Chrome' in which:
            return Remote(command_executor='http://0.0.0.0:4723/wd/hub', desired_capabilities=self.chrome_appium_desired_capadibilties())
        elif 'Nexar' in which:
            return Remote(command_executor='http://0.0.0.0:4723/wd/hub', desired_capabilities=self.nexar_appium_desired_capadibilties())
        else:
            raise ValueError()

    # def chrome_driver(self):
    #     return

    # def wait(self,a):
    #     if 'chrome' in a :
    #         return WebDriverWait(driver=webdriver.Chrome(executable_path=self.binary_path()), timeout=60)

class Interact(Toolbox):

    # def wait(self, _wait: WebDriverWait ,what_to_wait_for='', by='xpath'):
    #     if 'xpath' in by:
    #         # return _wait.until(ec.element_to_be_clickable((By.XPATH, what_to_wait_for)))
    #         _wait.until(ec.element_to_be_clickable((By.XPATH,what_to_wait_for)))

    def id(self, _id,new_driver: WebDriver,_wait: WebDriverWait,what_to_wait_for='') -> WebElement:
        try:
            _wait.until(ec.element_to_be_clickable((By.ID, what_to_wait_for)))
        except Exception as err:
            _wait.until(ec.text_to_be_present_in_element((By.ID, what_to_wait_for),'שכחת את כתובת האימייל?'))
        return new_driver.find_element_by_id(_id)

    def acc_id(self, _acc_id, new_driver: WebDriver, _wait: WebDriverWait, what_to_wait_for='') -> WebElement:
        _wait.until(ec.element_to_be_clickable((By.ACC_ID, what_to_wait_for)))
        return new_driver.find_element_by_accessibility_id(_acc_id)

    def xpath(self, _xpath,new_driver: WebDriver,_wait: WebDriverWait,what_to_wait_for='') -> WebElement:
        try:
            _wait.until(ec.element_to_be_clickable((By.XPATH, what_to_wait_for)))
        except Exception as err:
            _wait.until(ec.text_to_be_present_in_element((By.XPATH, what_to_wait_for),'שכחת את כתובת האימייל?'))
        return new_driver.find_element_by_xpath(_xpath)

    def all_visible(self,new_driver: WebDriver):
        return new_driver.find_elements_by_xpath(self.ALL_BY_XPATH)

    def clickID(self, _id,new_driver: WebDriver):
        self.id(_id,new_driver).click()

    def clickXpath(self, _xpath,new_driver: WebDriver):
        self.xpath(_xpath, new_driver).click()

    def ie(self, element: WebElement, is_sent_keys: bool, value=None):
        if is_sent_keys and value is not None:
            logger.info(f'typing on {element} with {value}')
            element.send_keys(value)
        elif is_sent_keys is False:
            logger.info(f'clicking on {element}')
            element.click()
        else:
            raise ValueError('invalid values for function')

    # def click_on_wanted_message(self,driver: WebDriver, which_message_title):  # Nexar Clal
    #     driver.start_session()
    #     driver.background_app(0.1)
    #     time.sleep(2)
    #     print(which_message_title)
    #     time.sleep(2)
    #     timer = 0
    #     while 1 and timer < 30:
    #         time.sleep(1)
    #         message_screen = driver.find_elements_by_xpath(self.ALL_BY_XPATH)
    #         for entity in message_screen:
    #             if entity.text == which_message_title:
    #                 print(f"found message{which_message_title}")
    #                 entity.click()
    #                 break
    #         timer += 1
    #         break
    #     time.sleep(2)

if __name__ == '__main__':
    interact = Interact()
    ident = interact.id('mobi.nexar.dashcam:id/actionBtn')
    interact.ie(ident, False)
