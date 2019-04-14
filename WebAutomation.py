from OtpExtractor import NexarOtpHandler as ExtractorRunner
from selenium import webdriver
import os
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller
from toolbox import Toolbox as tb
from toolbox import Interact
from loguru import logger
from strings import CH_XPATH as ch_bt
from strings import STRINGS as st

ALL_BY_XPATH = '//*[not(*)]'

class DashboardLogin(Interact):

    def __init__(self):
        self.keyboard = Controller()
        self.driver_auth = tb.driver(self, which='chrome')
        self.driver_auth.get('about:blank')
        self.wait = WebDriverWait(driver=self.driver_auth, timeout=60)


    def login_to_dashboard(self):


        self.driver_auth.get('https://dashboard.getnexar.com/admin/login')

        self.wait.until(
            ec.element_to_be_clickable((By.XPATH, ch_bt.LOG_IN_WITH_GOOGLE))
        )
        time.sleep(1)

        Interact.ie(self, element=Interact.xpath(self, ch_bt.LOG_IN_WITH_GOOGLE,'chrome'),is_sent_keys=False)

        # self.driver_auth.find_element_by_xpath(ch_bt.LOG_IN_WITH_GOOGLE).click()

        google_window = self.driver_auth.window_handles[1]
        self.driver_auth.switch_to.window(google_window)
        time.sleep(1)


        self.wait.until(ec.element_to_be_clickable((By.XPATH, ch_bt.MAIL_FIELD)))
        time.sleep(1)
        self.driver_auth.find_element_by_xpath(ch_bt.MAIL_FIELD).send_keys('qatesting@getnexar.com')

        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.NEXT_BUTTON)))
        time.sleep(1)
        self.driver_auth.find_element_by_xpath(ch_bt.NEXT_BUTTON).click() # click next after mail inside

        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.PASSWORD_GOOGLE)))
        time.sleep(1)
        self.driver_auth.find_element_by_xpath(ch_bt.PASSWORD_GOOGLE).send_keys('VroomVroom%') # set password

        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.PASSWORD_NEXT_BUTTON)))
        time.sleep(1)
        self.driver_auth.find_element_by_xpath(ch_bt.PASSWORD_NEXT_BUTTON).click()  # click next after pass inside

        google_window2 = self.driver_auth.window_handles[0]
        self.driver_auth.switch_to.window(google_window2)

    def enter_policy_details(self):

        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.POLICY_NUMBER)))
        self.driver_auth.find_element_by_xpath(ch_bt.POLICY_NUMBER).send_keys('+972535276570')

        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.POLICY_NAME)))
        self.driver_auth.find_element_by_xpath(ch_bt.POLICY_NAME).send_keys('test clal')

        self.wait.until( ec.element_to_be_clickable((By.XPATH,ch_bt.HOUSE_NUMBER)))
        self.driver_auth.find_element_by_xpath(ch_bt.HOUSE_NUMBER).send_keys('7')

        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.STREET)))
        self.driver_auth.find_element_by_xpath(ch_bt.STREET).send_keys('aliya')

        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.CITY)))
        self.driver_auth.find_element_by_xpath(ch_bt.CITY).send_keys('tlv')


        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.EXCEPTED_DRIVERS_LIST)))
        self.driver_auth.find_element_by_xpath(ch_bt.EXCEPTED_DRIVERS_LIST).click()

        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.ONE_EXCEPTED_DRIVER)))
        time.sleep(1)
        self.driver_auth.find_element_by_xpath(ch_bt.ONE_EXCEPTED_DRIVER).click()

        self.wait.until(ec.element_to_be_clickable((By.XPATH, ch_bt.CREATE_POLICY_BUTTON)))
        time.sleep(1)
        self.driver_auth.find_element_by_xpath(ch_bt.CREATE_POLICY_BUTTON).click()

        self.wait.until( ec.element_to_be_clickable((By.XPATH, ch_bt.DONE_AFTER_POLICY_SENT))) # DONE BUTTON
        logger.info("___POLICY SENT___")

    def send_policy_via_dashboard(self):

        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.DASHBOARD_VIEW_ALL_BUTTON)))

        time.sleep(1)
        self.driver_auth.find_element_by_xpath(ch_bt.DASHBOARD_VIEW_ALL_BUTTON).click()

        self.wait.until(ec.element_to_be_clickable((By.XPATH,ch_bt.DASHBOARD_CREATE_POLICY_BUTTON)))
        time.sleep(1)
        self.driver_auth.find_element_by_xpath(ch_bt.DASHBOARD_CREATE_POLICY_BUTTON).click()

        # -----------------------------------------------------------------------------------------------------------------------

        self.enter_policy_details()

    def delete_clal_driver(self):
        self.wait.until(
            ec.element_to_be_clickable((By.XPATH,
                                        '//*[@id="container"]/div/div/main/div[2]/div[2]/div[2]/div[3]'))
        )


        self.driver_auth.find_element_by_xpath('//*[@id="container"]/div/div/main/div[2]/div[2]/div[2]/div[3]').click()

        self.wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="container"]/div/div/main/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[2]'))) # click on first row on dashboard
        time.sleep(1)

        click_on_user = self.driver_auth.find_element_by_xpath('//*[@id="container"]/div/div/main/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[2]')
        click_on_user.click()

        self.wait.until(ec.new_window_is_opened)
        time.sleep(1)

        policy_owner_name_placeHolder = self.driver_auth.find_element_by_xpath('//*[@id="container"]/div/div/main/div/div[2]/div[2]/div[2]/div/div[2]/div[4]')
        if 'test clal' in policy_owner_name_placeHolder.text:
            all_remove_elements = self.driver_auth.find_elements_by_xpath(ALL_BY_XPATH)
            for to_remove in all_remove_elements:
                if 'REMOVE DRIVER' in to_remove.text:
                    to_remove.click()
                    # i=i+1
                    time.sleep(10)
                    # if i=2:

                    break
                    # self.keyboard.press(Key.enter)
                    # time.sleep(2)
                    # self.keyboard.release(Key.enter)


            # time.sleep(3)


if __name__ == '__main__':
    test_login = DashboardLogin()
    init_clal = ExtractorRunner()

    test_login.login_to_dashboard()

    test_login.send_policy_via_dashboard()

    test_login.driver_auth.close()

    init_clal.click_on_wanted_message("Nexar Clal")
    init_clal.link_extractor_to_chrome()

    init_clal.nexar_onboarding()

    init_clal.continue_when_clal()

    init_clal.log_out_from_nexar()

    init_clal.delete_message_by_name("Nexar Clal")

    test_teardown = DashboardLogin()

    test_teardown.login_to_dashboard()
    test_teardown.delete_clal_driver()

    test_teardown.driver_auth.close()
    # init_clal.appium_driver.close()Z
