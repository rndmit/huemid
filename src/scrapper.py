import os
import logging
import base64
import pathlib
import time
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from anticaptchaofficial.imagecaptcha import imagecaptcha
import config


START_PAGE = 'https://alma-ata.kdmid.ru/queue/OrderInfo.aspx'


class Scrapper():
    def __init__(self) -> None:
        self.logger = logging.getLogger("main")
        self.logger.info('Initializing Scrapper')
        opts = FirefoxOptions()
        opts.headless = True
        self.browser = Firefox(options=opts)

        self.solver = imagecaptcha()
        self.solver.set_verbose(0)
        self.solver.set_numeric(1)
        self.solver.set_case(False)
        self.solver.set_math(False)
        self.solver.set_phrase(False)
        self.solver.set_key(config.ANTI_CAPTCHA_KEY)

    def __del__(self) -> None:
        self.logger.info('Cleaning up Scrapper')
        self.browser.quit()

    def run(self, run_id: str) -> None:
        self.logger.info(f'Run {run_id} started')
        self.browser.get(START_PAGE)
        WebDriverWait(self.browser, 240).until(
            lambda x: x.find_element(By.ID, 'ctl00_MainContent_imgSecNum'))

        self.logger.debug('Filling creds')
        self.fill_creds()

        captcha_dst = pathlib.PurePath(os.getcwd(), 'captchas', run_id).with_suffix('.png')
        self.logger.debug(f'Extracting captcha to {captcha_dst}')
        self.extract_captcha(captcha_dst)
        self.logger.info(f'Solving captcha {captcha_dst}')
        captcha_result = self.solver.solve_and_return_solution(captcha_dst)
        self.browser.find_element(By.ID, 'ctl00_MainContent_txtCode').send_keys(captcha_result)
        self.logger.info(f'Captcha solved: {captcha_result}')

        self.browser.find_element(By.ID, 'ctl00_MainContent_ButtonA').click()
        self.browser.find_element(By.ID, 'ctl00_MainContent_ButtonB').click()

        result_dst = pathlib.PurePath(os.getcwd(), 'results', run_id).with_suffix('.png')
        self.logger.info(f'Saving result to {result_dst}')
        self.browser.get_full_page_screenshot_as_file(result_dst.__str__())
        self.logger.info(f'Run {run_id} finished')
        return

    def extract_captcha(self, dst: str) -> None:
        captcha_el = self.browser.find_element(By.ID, 'ctl00_MainContent_imgSecNum')
        img_captcha_base64 = self.browser.execute_async_script("""
            var el = arguments[0], callback = arguments[1];
            el.addEventListener('load', function fn(){
              el.removeEventListener('load', fn, false);
              var cnv = document.createElement('canvas');
              cnv.width = this.width+100; cnv.height = this.height+20;
              cnv.getContext('2d').drawImage(this, 0, 0);
              callback(cnv.toDataURL('image/jpeg').substring(22));
            }, false);
            el.dispatchEvent(new Event('load'));
            """, captcha_el)
        with open(dst, 'wb') as f:
            f.write(base64.b64decode(img_captcha_base64))

    def fill_creds(self) -> None:
        order_num_field = self.browser.find_element(By.ID, 'ctl00_MainContent_txtID')
        order_num_field.send_keys(config.ORDER_NUM)
        sec_code_field = self.browser.find_element(By.ID, 'ctl00_MainContent_txtUniqueID')
        sec_code_field.send_keys(config.SECURITY_CODE)
