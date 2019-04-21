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
        self.wait = WebDriverWait(driver=self.driver_auth, timeout=10)


    def login_to_dashboard(self):

        self.driver_auth.get('https://dashboard.getnexar.com/admin/login')

        Interact.ie(self, element=Interact.xpath(self, ch_bt.LOG_IN_WITH_GOOGLE, self.driver_auth,self.wait,ch_bt.LOG_IN_WITH_GOOGLE), is_sent_keys=False,value=None)

        google_window = self.driver_auth.window_handles[1]

        self.driver_auth.switch_to.window(google_window)

        time.sleep(2)

        Interact.ie(self,element=Interact.xpath(self, ch_bt.MAIL_FIELD, self.driver_auth,self.wait,what_to_wait_for=ch_bt.FORGOT_PASSWORD_GOOGLE_LOGIN_BUTTON), is_sent_keys=True, value='qatesting@getnexar.com')

        Interact.ie(self,element=Interact.xpath(self,ch_bt.NEXT_BUTTON,self.driver_auth,self.wait,what_to_wait_for=ch_bt.NEXT_BUTTON), is_sent_keys=False,value=None)

        Interact.ie(self,element=Interact.xpath(self, ch_bt.PASSWORD_GOOGLE, self.driver_auth,self.wait,what_to_wait_for=ch_bt.PASSWORD_NEXT_BUTTON), is_sent_keys=True, value='%')

        Interact.ie(self,element=Interact.xpath(self,ch_bt.PASSWORD_NEXT_BUTTON,self.driver_auth,self.wait,what_to_wait_for=ch_bt.PASSWORD_NEXT_BUTTON), is_sent_keys=False,value=None)

        time.sleep(2)

        google_window2 = self.driver_auth.window_handles[0]
        self.driver_auth.switch_to.window(google_window2)

    def enter_policy_details(self):

        Interact.ie(self,element=Interact.xpath(self,ch_bt.POLICY_NUMBER,self.driver_auth,self.wait,what_to_wait_for=ch_bt.POLICY_NUMBER), is_sent_keys=True, value='+972535276570')

        Interact.ie(self, element=Interact.xpath(self, ch_bt.POLICY_NAME, self.driver_auth,self.wait,what_to_wait_for=ch_bt.POLICY_NAME), is_sent_keys=True,value='test clal')

        Interact.ie(self, element=Interact.xpath(self, ch_bt.HOUSE_NUMBER, self.driver_auth,self.wait,what_to_wait_for=ch_bt. HOUSE_NUMBER), is_sent_keys=True,value='7')

        Interact.ie(self, element=Interact.xpath(self, ch_bt.STREET, self.driver_auth,self.wait,what_to_wait_for=ch_bt.STREET), is_sent_keys=True,value='Aliya')

        Interact.ie(self, element=Interact.xpath(self, ch_bt.CITY, self.driver_auth,self.wait,what_to_wait_for=ch_bt.CITY), is_sent_keys=True,value='TLV')

        # --------------------------------------------------------------------------------------------------------------

        Interact.ie(self,element=Interact.xpath(self,ch_bt.EXCEPTED_DRIVERS_LIST,self.driver_auth,self.wait,what_to_wait_for=ch_bt.EXCEPTED_DRIVERS_LIST), is_sent_keys=False,value=None)

        Interact.ie(self,element=Interact.xpath(self,ch_bt.ONE_EXCEPTED_DRIVER,self.driver_auth,self.wait,what_to_wait_for=ch_bt.ONE_EXCEPTED_DRIVER), is_sent_keys=False,value=None)

        Interact.ie(self,element=Interact.xpath(self,ch_bt.CREATE_POLICY_BUTTON,self.driver_auth,self.wait,what_to_wait_for=ch_bt.CREATE_POLICY_BUTTON), is_sent_keys=False,value=None)

        self.wait.until( ec.element_to_be_clickable((By.XPATH, ch_bt.DONE_AFTER_POLICY_SENT))) # DONE BUTTON
        logger.info("___POLICY SENT___")

    def send_policy_via_dashboard(self):

        Interact.ie(self,element=Interact.xpath(self,ch_bt.DASHBOARD_VIEW_ALL_BUTTON,self.driver_auth,self.wait,what_to_wait_for=ch_bt.DASHBOARD_VIEW_ALL_BUTTON), is_sent_keys=False,value=None)

        Interact.ie(self,element=Interact.xpath(self,ch_bt.DASHBOARD_CREATE_POLICY_BUTTON,self.driver_auth,self.wait,what_to_wait_for=ch_bt.DASHBOARD_CREATE_POLICY_BUTTON), is_sent_keys=False,value=None)

        # -----------------------------------------------------------------------------------------------------------------------

        self.enter_policy_details()

    def delete_clal_driver(self):
        Interact.ie(self,element=Interact.xpath(self,ch_bt.DASHBOARD_VIEW_ALL_BUTTON,self.driver_auth,self.wait,what_to_wait_for=ch_bt.DASHBOARD_VIEW_ALL_BUTTON), is_sent_keys=False,value=None)

        Interact.ie(self,element=Interact.xpath(self,ch_bt.FIRST_TEAM_BUTTON,self.driver_auth,self.wait,what_to_wait_for=ch_bt.FIRST_TEAM_BUTTON), is_sent_keys=False,value=None)

        self.wait.until(ec.new_window_is_opened)
        time.sleep(1)

        policy_owner_name_placeHolder = self.driver_auth.find_element_by_xpath(ch_bt.NAME_OF_POLICY_OWNER_AFTER_POLICY_CREATED)
        if 'test clal' in policy_owner_name_placeHolder.text:
            all_remove_elements = self.driver_auth.find_elements_by_xpath(ALL_BY_XPATH)
            for to_remove in all_remove_elements:
                if 'REMOVE DRIVER' in to_remove.text:
                    to_remove.click()
                    time.sleep(10)
                    break
        alert = self.driver_auth.switch_to.alert
        alert.accept()
        time.sleep(4)



if __name__ == '__main__':
    counter_success = 0
    counter_failure = 0
    for i in range(2):

        try:
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
            #
            test_teardown.login_to_dashboard()
            test_teardown.delete_clal_driver()

            test_teardown.driver_auth.close()
            init_clal.nexar_driver.close_app()
            counter_success += 1
        except Exception:
            counter_failure += 1

    logger.info(counter_success)
    logger.info(counter_failure)

