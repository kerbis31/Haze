from appium.webdriver import Remote
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from loguru import logger
from selenium import webdriver
import os
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from appium.webdriver.webdriver import WebDriver

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

    def chrome_driver(self):
        return

class Interact(Toolbox):

    def id(self, _id, _which) -> WebElement:
        return self.driver(which=_which).find_element_by_id(_id)

    def xpath(self, _xpath, _which) -> WebElement:
        return self.driver(which=_which).find_element_by_xpath(_xpath)

    def all_visible(self,_which):
        return self.driver(which=_which).find_elements(self.ALL_BY_XPATH)

    def clickID(self, _id):
        self.id(_id).click()

    def clickXpath(self, _xpath):
        self.xpath(_xpath).click()

    def ie(self, element: WebElement, is_sent_keys: bool , value = None):
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
