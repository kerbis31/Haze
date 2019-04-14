import re
from appium import webdriver
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os
from toolbox import Interact
from toolbox import Toolbox as tb
from loguru import logger
from strings import BUTTONS as bt
from strings import STRINGS as st

apk = os.path.join(os.environ['HOME'], 'Downloads', 'app-consumer-release.apk')
ALL_BY_XPATH = '//*[not(*)]'

class NexarOtpHandler(Interact):


    def __init__(self):
        self.nexar_driver = tb.driver(self, which='Nexar')
        self.wait = WebDriverWait(self.nexar_driver, timeout=40)
        self.value = None
##--------------- VBJIO --------------------------------------------------------------------------------------

    def enter_login_details(self):
        name_for_login = self.nexar_driver.find_element_by_id(bt.name_for_login)
        name_for_login.send_keys("test clal")

        phone_for_login = self.nexar_driver.find_element_by_id(st.phone_for_login)
        phone_for_login.send_keys("+972535276570")

        sign_up_button = self.nexar_driver.find_element_by_id(bt.SIGN_UP_BUTTON)
        sign_up_button.click()

        self.wait.until(ec.element_to_be_clickable((By.ID, bt.re_send_otp)))

    def click_on_wanted_message(self, which_message_title):# Nexar Clal
        self.nexar_driver.start_session(tb.sms_appium_desired_capabilities())
        self.nexar_driver.background_app(0.1)
        time.sleep(2)
        logger.info(which_message_title)
        time.sleep(2)

        timer = 0
        message_found_indicator = 0

        while timer < 6 and message_found_indicator == 0:
            time.sleep(1)
            timer += 1
            message_screen = self.nexar_driver.find_elements_by_xpath(ALL_BY_XPATH)
            for entity in message_screen:
                if entity.text == which_message_title:
                    logger.info("Message found")
                    message_found_indicator = 1
                    entity.click()
                    break

    def link_extractor_to_chrome(self):
        self.wait.until(ec.element_to_be_clickable((By.ID, bt.SMS_TOP_TITLE)))
        text_message = self.nexar_driver.find_element_by_id(bt.message_text)
        splited_message = text_message.text.split()
        for url_to_copy in splited_message:
            if url_to_copy.startswith("https"):
                logger.info(url_to_copy)
                break
        self.nexar_driver.start_session(tb.chrome_appium_desired_capadibilties())
        self.nexar_driver.get(url_to_copy)
        time.sleep(3)

    def otp_extractor_from_notifications(self, stri): #into Nexar

        logger.info(stri)
        self.nexar_driver.open_notifications()
        self.wait.until(ec.presence_of_element_located((By.ID, st.MESSAGES_ELEMENT_NOTIFICATIONS)))

        notification_entities = self.nexar_driver.find_elements_by_xpath(ALL_BY_XPATH)
        for entity in notification_entities:
            if entity.text == 'Messages':
                logger.info("Found messages section")
                entity.click()
                messages_entities = self.nexar_driver.find_elements_by_xpath(ALL_BY_XPATH)
                for message in messages_entities:
                    if stri in message.text:
                        self.value = re.findall("\d+", message.text)
                        logger.info("We have otp")
                        break
                break

    def check_if_clal_user_onboarded_sucsessfully(self):
        time.sleep(2)
        try:
            self.wait.until(ec.element_to_be_clickable((By.ID, bt.CLAL_GOT_IT)))
            logger.info("CLAL screen found")
        except Exception as err:
            try:
                self.wait.until((ec.element_to_be_clickable((By.XPATH, bt.TOP_LEFT_MENU))))
                logger.info("clal screen didnt shpw up")
            except Exception as another_err:
                raise ValueError

    def continue_when_clal(self):
        time.sleep(2)
        try:
            self.wait.until(ec.element_to_be_clickable((By.ID, bt.CLAL_GOT_IT)))
            got_it_button = self.nexar_driver.find_element_by_id(bt.CLAL_GOT_IT)
            got_it_button.click()
            logger.info("CLAL screen found")
        except Exception as err:
            try:
                self.wait.until((ec.element_to_be_clickable((By.XPATH, bt.TOP_LEFT_MENU))))
                logger.info("clal screen didnt shpw up")
            except Exception as another_err:
                raise ValueError

    def pass_nexar_permissions(self):
        self.nexar_driver.background_app(0.1)
        for i in range(3):
            time.sleep(2)
            self.wait.until(ec.element_to_be_clickable((By.ID, bt.ACTION)))

            enable_button = self.nexar_driver.find_element_by_id(bt.ACTION)
            enable_button.click()

            self.wait.until(ec.element_to_be_clickable((By.ID, bt.ALLOW)))

            allow_enable_button = self.nexar_driver.find_element_by_id(bt.ALLOW)
            allow_enable_button.click()

            self.nexar_driver.background_app(0.1)

    def nexar_onboarding(self):

        os.system(st.reset_perm_script) #RESET ALL NEXAR PERMISSIONS BY SCRIPT

        self.nexar_driver.start_session(tb.nexar_appium_desired_capadibilties())

        self.pass_nexar_permissions()

        self.enter_login_details()

        self.otp_extractor_from_notifications("into Nexar")

        self.nexar_driver.press_keycode(4)

        self.nexar_driver.background_app(0.1)

        try:
            self.enter_login_details()
        except Exception as err:
            self.wait.until(ec.element_to_be_clickable((By.ID, bt.RESEND_OTP)))

        self.nexar_driver.find_element_by_id(st.PIN_CODE_UI).send_keys(self.value)

        self.nexar_driver.find_element_by_id(bt.LOGIN_BUTTON).click()

        self.wait.until(ec.element_to_be_clickable((By.XPATH, bt.AGREE_TOS)))

        self.nexar_driver.find_element_by_xpath(bt.AGREE_TOS).click()

    def log_out_from_nexar(self):
        self.nexar_driver.background_app(0.1)

        self.wait.until(ec.element_to_be_clickable((By.XPATH, bt.TOP_LEFT_MENU)))
        self.nexar_driver.find_element_by_accessibility_id(st.TOP_MENU_ACC_ID).click()

        menu_enteties = self.nexar_driver.find_elements_by_xpath(ALL_BY_XPATH)
        logger.info(menu_enteties)
        for entity in menu_enteties:
            if entity.text == 'Log out':
                entity.click()
                logger.info('Success to logout')
                break

    def delete_message_after_clicked(self):
        self.nexar_driver.find_element_by_accessibility_id(st.IN_MESSAGE_MENU_ACC_ID).click()
        time.sleep(1)

        menu_enteties = self.nexar_driver.find_elements_by_xpath(ALL_BY_XPATH)
        for entity in menu_enteties:
            if entity.text == 'Delete':
                logger.info('Sucsses')
                entity.click()
                # time.sleep(1)
                self.wait.until(ec.element_to_be_clickable((By.ID,bt.DELETE_MESSAGE_POPUP)))
                self.nexar_driver.find_element_by_id(bt.DELETE_MESSAGE_POPUP).click()
                break

    def delete_message_by_name(self, sms_to_delete): #need to get rid of wait
        self.click_on_wanted_message(sms_to_delete)
        self.delete_message_after_clicked()

if __name__ == '__main__':
    test_login = NexarOtpHandler()
    test_login.click_on_wanted_message("Nexar Clal")
    test_login.link_extractor_to_chrome()
    test_login.nexar_onboarding()
    test_login.continue_when_clal()
    test_login.log_out_from_nexar()
    test_login.delete_message_by_name("Nexar Clal")


