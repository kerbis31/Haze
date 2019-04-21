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
        Interact.ie(self,element=Interact.id(self,bt.name_for_login,self.nexar_driver,self.wait,what_to_wait_for=bt.name_for_login), is_sent_keys=True,value='test clal')

        Interact.ie(self,element=Interact.id(self,st.phone_for_login,self.nexar_driver,self.wait,what_to_wait_for=st.phone_for_login), is_sent_keys=True,value='+972535276570')

        Interact.ie(self,element=Interact.id(self,bt.SIGN_UP_BUTTON,self.nexar_driver,self.wait,what_to_wait_for=bt.SIGN_UP_BUTTON), is_sent_keys=False,value=None)

        self.wait.until(ec.element_to_be_clickable((By.ID, bt.re_send_otp)))

    def click_on_wanted_message(self, which_message_title):# Nexar Clal
        self.nexar_driver.start_session(tb.sms_appium_desired_capabilities())
        logger.info(which_message_title)
        timer = 0
        message_found_indicator = 0

        try:
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
        except Exception as err:
            self.click_on_wanted_message(which_message_title)

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

        notification_entities = Interact.all_visible(self, new_driver=self.nexar_driver)
        # notification_entities = self.nexar_driver.find_elements_by_xpath(ALL_BY_XPATH)
        for entity in notification_entities:
            if entity.text == 'Messages':
                logger.info("Found messages section")
                entity.click()
                messages_entities = self.nexar_driver.find_elements_by_xpath(ALL_BY_XPATH)
                for message in messages_entities:
                    if stri in message.text:
                        self.value = re.findall("\d+", message.text)
                        logger.info(f"We have otp: {self.value}")
                        break
                break

    def continue_when_clal(self):
        time.sleep(2)
        try:
            Interact.ie(self, element=Interact.id(self, bt.CLAL_GOT_IT, self.nexar_driver, self.wait,what_to_wait_for=bt.CLAL_GOT_IT), is_sent_keys=False)
            logger.info("CLAL screen found")
        except Exception as err:
            try:
                self.wait.until((ec.element_to_be_clickable((By.XPATH, bt.TOP_LEFT_MENU))))
                logger.info("clal screen didnt show up")
            except Exception as another_err:
                raise ValueError

    def pass_nexar_permissions(self):
        self.nexar_driver.background_app(0.1)
        for i in range(3):

            Interact.ie(self, element=Interact.id(self, bt.ACTION, self.nexar_driver, self.wait, what_to_wait_for=bt.ACTION), is_sent_keys=False)
            Interact.ie(self, element=Interact.id(self, bt.ALLOW, self.nexar_driver, self.wait, what_to_wait_for=bt.ALLOW), is_sent_keys=False)

            self.nexar_driver.background_app(0.1)

    def log_out_from_nexar(self):
        self.nexar_driver.background_app(0.1)
        Interact.ie(self, element=Interact.xpath(self, bt.TOP_LEFT_MENU, self.nexar_driver, self.wait, what_to_wait_for=bt.TOP_LEFT_MENU),is_sent_keys=False)

        menu_enteties = self.nexar_driver.find_elements_by_xpath(ALL_BY_XPATH)
        logger.info(menu_enteties)
        for entity in menu_enteties:
            if entity.text == 'Log out':
                entity.click()
                logger.info('Success to logout')
                break

    def delete_message_after_clicked(self):
        Interact.ie(self, element=Interact.acc_id(self, st.IN_MESSAGE_MENU_ACC_ID, self.nexar_driver, self.wait,what_to_wait_for=st.IN_MESSAGE_MENU_ACC_ID), is_sent_keys=False)

        time.sleep(1)

        menu_enteties = Interact.all_visible(self,new_driver= self.nexar_driver)

        for entity in menu_enteties:

            if entity.text == 'Delete':
                logger.info('Sucsses')
                entity.click()
                Interact.ie(self, element=Interact.id(self, bt.DELETE_MESSAGE_POPUP, self.nexar_driver, self.wait,what_to_wait_for=bt.DELETE_MESSAGE_POPUP), is_sent_keys=False)
                break

    def delete_message_by_name(self, sms_to_delete):
        self.click_on_wanted_message(sms_to_delete)
        self.delete_message_after_clicked()

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

        Interact.ie(self, element=Interact.id(self, st.PIN_CODE_UI, self.nexar_driver, self.wait, what_to_wait_for=bt.re_send_otp), is_sent_keys=True, value=self.value)

        Interact.ie(self, element=Interact.id(self, bt.LOGIN_BUTTON, self.nexar_driver, self.wait, what_to_wait_for=bt.LOGIN_BUTTON), is_sent_keys=False)

        Interact.ie(self, element=Interact.xpath(self, bt.AGREE_TOS, self.nexar_driver, self.wait, what_to_wait_for=bt.AGREE_TOS), is_sent_keys=False)


if __name__ == '__main__':
    test_login = NexarOtpHandler()
    test_login.click_on_wanted_message("Nexar Clal")
    test_login.link_extractor_to_chrome()
    test_login.nexar_onboarding()
    test_login.continue_when_clal()
    test_login.log_out_from_nexar()
    test_login.delete_message_by_name("Nexar Clal")


