import datetime
from time import sleep
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

s = Service(executable_path='C:/Automation/Python/parabank/chromedriver.exe')
driver = webdriver.Chrome(service=s)
fake = Faker(locale=['en_CA', 'en_US'])

# --------------------------------- LOCATORS ---------------------------------
app = 'Parabank'
app_url = 'https://parabank.parasoft.com/'
app_home_page_url = 'https://parabank.parasoft.com/parabank/index.htm'
app_home_page_title = 'ParaBank | Welcome | Online Banking'
register_page_url = 'https://parabank.parasoft.com/parabank/register.htm'
register_page_title = 'ParaBank | Register for Free Online Account Access'

first_name = fake.first_name()
last_name = fake.last_name()
full_name = f'{first_name} {last_name}'
address = fake.street_address()
city = fake.city()
state = fake.province_abbr()
zip_code = fake.postalcode()
phone = fake.bothify(text='1-(###)-###-####')
ssn = fake.ssn()
username = f'{fake.user_name()}{fake.pyint(111,999)}'
password = fake.password()

field_id = ['customer.firstName', 'customer.lastName', 'customer.address.street', 'customer.address.city',
            'customer.address.state', 'customer.address.zipCode', 'customer.phoneNumber', 'customer.ssn',
            'customer.username', 'customer.password', 'repeatedPassword']

field_val = [first_name, last_name, address, city, state, zip_code, phone, ssn, username, password, password]

# ----------------------------------------------------------------------------

def setUp():
    print(f'Launch {app} App')
    print(' ---------------------- ~*~ -----------------------------')
    driver.maximize_window()
    driver.implicitly_wait(30)
    driver.get(app_url)
    if app_home_page_url in driver.current_url and driver.title == app_home_page_title:
        print(f'{app} App launched successfully!')
        print(f'{app} Homepage URL: {driver.current_url}, {app} Homepage title: {driver.title}')
        sleep(0.25)
    else:
        print(f'{app} App did not launch. Check your code or application')
        print(f'Current URL: {driver.current_url}, Current Page title: {driver.title}')
        tearDown()


def tearDown():
    if driver is not None:
        print(' --------------------- ~*~ ---------------------------')
        print(f'The test is completed at: {datetime.datetime.now()}')
        sleep(0.25)
        driver.close()
        driver.quit()


def register():
    print(' ------------------------ ~*~ ----------------------------')
    if app_home_page_url in driver.current_url:
        driver.find_element(By.LINK_TEXT, 'Register').click()
        if register_page_url in driver.current_url and driver.title == register_page_title:
            print(f' --- {app} App Registration page is displayed.')
            print(f' --- Registration page URL: {register_page_url}, Registration page title: {register_page_title}')
            sleep(0.25)
            assert driver.find_element(By.XPATH, '//h1[contains(., "Signing up is easy!")]').is_displayed()
            sleep(0.25)
            for i in range(len(field_id)):
                fid, val = field_id[i], field_val[i]
                driver.find_element(By.ID, fid).send_keys(val)
                sleep(0.25)
            driver.find_element(By.XPATH, '//input[@value="Register"]').click()
            sleep(0.25)
            assert driver.find_element(By.XPATH, f'//p[contains(., "Welcome {full_name}")]').is_displayed() \
                   and driver.find_element(By.XPATH, f'//h1[contains(., "Welcome {username}")]').is_displayed()
            reg_check = driver.find_element(By.XPATH, f'//p[contains(., "Welcome {full_name}")]').is_displayed() \
                   and driver.find_element(By.XPATH, f'//h1[contains(., "Welcome {username}")]').is_displayed()
            #print(reg_check)
            sleep(0.25)
            if reg_check:
                print(f' --- Customer {full_name} is registered.')
                sleep(0.25)
            else:
                print(f' --- Registration failed. Please try again.')



def log_out():
    print(' ----------------------- ~*~ ---------------------------')
    driver.find_element(By.LINK_TEXT, 'Log Out').click()
    sleep(0.25)
    if app_home_page_url in driver.current_url:
        assert driver.find_element(By.XPATH, '//h2[contains(., "Customer Login")]').is_displayed()
        print(f' --- Logout successful! {datetime.datetime.now()}')


def log_in():
    print(' ---------------------- ~*~ ----------------------------')
    if app_home_page_url in driver.current_url:
        print(f' --- {app} Homepage is displayed.')
        sleep(0.25)
        driver.find_element(By.NAME, 'username').send_keys(username)
        sleep(0.25)
        driver.find_element(By.NAME, 'password').send_keys(password)
        sleep(0.25)
        driver.find_element(By.XPATH, '//input[@value="Log In"]').click()
        sleep(0.5)
        try:
            assert driver.find_element(By.XPATH, f'//p[contains(., "Welcome {full_name}")]').is_displayed()
            print(f' --- Customer {full_name} successfully login.')
            sleep(0.5)
        except NoSuchElementException as exception:
            print(f' --- Login is not successful. Please try again.')


# setUp()
# register()
# log_out()
# log_in()
# log_out()
# tearDown()
