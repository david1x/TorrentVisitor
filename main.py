<<<<<<< HEAD
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from dataclasses import dataclass
from dotenv import load_dotenv
import logging
import pyotp
import time
import re
import os

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

load_dotenv()

@dataclass
class ChromeDriver:
    """Data class for configuring ChromeDriver and Selenium."""
    driver_path: any = ChromeDriverManager().install()
    chrome_options: Options = None
    selenium_grid_url: str = None
    
    def create_chrome_driver(self):
        """Create a webdriver.Chrome instance with the specified configurations."""
        logging.info('Loading Chrome Driver')
        service = Service(self.driver_path)
        return webdriver.Chrome(service=service, options=self.chrome_options)
    
    def is_driver_valid(self, driver):
        logging.info('Validating Driver...')
        if (driver.current_url):
            logging.info('Driver is valid')
            return True
        else:
            logging.error('Driver is not valid')
            return False
    
    
@dataclass
class Website:
    urls: list
    title: str
    elements: dict
    pattern: str
    driver: ChromeDriver = None
    
    
    def isBrowserAlive(self) -> bool:
        logging.info("Checking if browser is open")
        if (self.driver.title == self.title):
            logging.info("Browser is open")
            return True
        logging.error("Browser is not open")
        return False

    def getNumberOfDaysVisited(self) -> str:
        logging.info("Getting The number of days user has visited TorrentLeech")
        try:
            preNumOfDays: str
            cells = self.driver.find_element(By.XPATH, self.elements['numDaysVisit'])
            matches = []
            for cell in cells:
                text = cell.text.strip()
                if re.match(self.pattern, text):
                    matches.append(text)
                    preNumOfDays = text

            if matches:
                logging.info(f"Found matching values: {matches}")

            else:
                logging.error("No matching values found.")
                exit(1)
                
        except:
            logging.error(f"Couldn't find the requested element. Trying Again with a different element")
            # preNumOfDays: str = self.driver.find_element(By.XPATH, self.elements['numDaysVisit']).text
        numOfDays: str = preNumOfDays.split(" / ")[0]
        return numOfDays
        
        
@dataclass
class Credential:
    username: str
    password: str
    otp_key: str = None
    driver: ChromeDriver = None
    website: Website = None
    
    def otp_current_code(self, key):
        return pyotp.TOTP(key).now()
    
    def enter_credentials(self):
        logging.info('Entering Credentials')
        time.sleep(5)
        user = self.driver.find_element(by="name", value="username")
        password = self.driver.find_element(by="name", value="password")
        user.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        
        logging.info('Getting OTP Code for Login')
        code = self.otp_current_code(self.otp_key)
        # time.sleep(30) 
        self.driver.find_element(By.XPATH, self.website.elements['otp']).send_keys(code)
        time.sleep(0.4)
        self.driver.find_element(By.XPATH, self.website.elements['login-btn']).send_keys(Keys.RETURN)
        logging.info(f'Current URL: {self.driver.current_url}')
        time.sleep(5)
        return

    def validate_login(self):
        logging.info('Checking if login passed')
        status = self.driver.current_url
        logging.info('status: ' + status)
        time.sleep(5)
        if 'torrents/top/index' not in status:
            if (self.driver.find_element(By.XPATH, self.website.elements['otp-auth-error-check']).text):
                logging.error("Authentication failed. Trying again... ")
                self.enter_credentials()
                return self.validate_login()
        logging.info('Login passed')    
        return True
        

def main() -> None:
    logging.info('Starting Script')
    logging.info('This script will run in headless mode')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # Disable the DevTools console output
    chrome_options.add_argument('--no-sandbox')  
    chrome_options.add_argument('--disable-dev-shm-usage') 
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
    chrome_options.add_argument('--headless')  # Add this line for headless mode
    # if chrome_options.headless:
        # logging.info('This script is running in headless mode')
    

    
    chrome_driver = ChromeDriver(chrome_options=chrome_options)
    driver = chrome_driver.create_chrome_driver()
    url = f'https://www.torrentleech.me'
    
    if not (chrome_driver.is_driver_valid(driver)):
        exit(1)

    website = Website(
        urls=[
            f'{url}/user/account/login/',
            f'{url}/profile/{os.getenv("TOR_USER")}/achievements'
        ],
        # //*[@id="prefcode"]
        title='TorrentLeech.org',
        elements={
            'otp':'//*[@id="prefcode"]/input[1]',
            'login-btn':'//*[@id="site-canvas"]/div[2]/div/div/section/form/div[2]/button',
            'otp-auth-error-check':'//*[@id="site-canvas"]/div[2]/div[1]/div/section/p',
            'numDaysVisit': '//table/tbody/tr/td[3]',
            },
        driver=driver,
        pattern=r"^\d+ / 365$"
    )
    
    website.isBrowserAlive()
    
    logging.info('Loading credentials from environment variables')
    creds = Credential(
        username = os.getenv('TOR_USER'),
        password = os.getenv('TOR_PASS'),
        otp_key = os.getenv('OTP_KEY'),
        driver = driver,
        website = website
    )
     
    logging.info(f'Loading URL: {website.urls[0]} to driver')
    driver.get(website.urls[0])
    logging.info(f'URL: {driver.current_url} loaded successfully')
    
    creds.enter_credentials()
    creds.validate_login()
  
    if not (website.isBrowserAlive()):
        logging.error("Driver was closed for unknown reason.")
        logging.error("Terminating program.")
        exit(1)
        
    logging.info(f'Loading Final URL: {website.urls[1]} to driver')
    driver.get(website.urls[1])
    logging.info(f'URL: {driver.current_url} loaded successfully')
    
    logging.info(f"Current Number of days visited on TorrentLeech: {website.getNumberOfDaysVisited()}")
    
    driver.refresh()
    driver.quit()
    logging.info("Program finished successfully!!!")
    exit(0)
        
    
if __name__ == "__main__":
    main()