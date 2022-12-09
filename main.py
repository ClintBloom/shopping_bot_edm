from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup

from account import check_file
from time import sleep


options = Options()
options.headless = False
driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)

_website = ''

first_item = '//*[@id="shopify-section-collection-template"]/div[1]/div[1]'
tag_items = 'product-item__meta__inner'
tag_title = 'product-item__title'
tag_sold_out = 'product-item__sold-out'
tag_add_cart = '#AddToCart-product-template'
tag_check_out = '#CartContainer > form > div.ajaxcart__footer.ajaxcart__footer--fixed > button'
tag_to_payment = '#continue_button'
tag_navigation = '#shopify-section-collection-template > div.pagination'
tag_next_button = '#shopify-section-collection-template > div.pagination > span.next'

input_email = '#checkout_email'
input_first_name = '#checkout_shipping_address_first_name'
input_last_name = '#checkout_shipping_address_last_name'
input_address = '#checkout_shipping_address_address1'
input_city = '#checkout_shipping_address_city'
input_state = '#checkout_shipping_address_province'
input_zip = '#checkout_shipping_address_zip'

input_card = '#number'
input_card_name = '#name'
input_card_exp = '#expiry'
input_card_security = '#verification_value'
same_as_shipping = '#checkout_different_billing_address_false'
pay_now = '#continue_button'


def main():
    file = check_file()
    # item_name = input('What are you searching for? ')
    item_name = []
    driver.get(_website)
    print('Started \n Loading Webpage and waiting for first item')

    finding_first_item = True
    while finding_first_item:
        try:
            WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.XPATH, first_item)))
            print('First pos found')
            finding_first_item = False
        except:
            print('No first pos item retrying')
            driver.refresh()

    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        page_amount = int(soup.find(class_='pagination').find_all(class_='page')[-1].text)
    except:
        page_amount = 1
        print('Single Page')

    # find all items on certain page
    items = []
    for page in range(1, page_amount + 1):
        if page != 1:
            driver.get('website{page}')
            WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.XPATH, first_item)))

        find_products = driver.find_elements(By.CLASS_NAME, 'product-item__link')
        for product in find_products:
            print(product.get_attribute('href'))
            items.append(product.get_attribute('href'))

    for title in items:
        if item_name[0].lower() in title:
            if len(item_name) >= 2:

                if item_name[1].lower() in title:
                    if len(item_name) >= 3:

                        if item_name[2].lower() in title:
                            print('goto page3', title)
                            driver.get(title)
                            break

                    else:
                        print('goto page2', title)
                        driver.get(title)
                        break

            else:
                print('goto page1', title)
                driver.get(title)
                break

    # Cart Check out phase
    add_cart_element = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, tag_add_cart)))
    add_cart_element.click()

    check_out_element = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, tag_check_out)))
    sleep(1.5)
    check_out_element.click()

    # Enter Shipping Info
    WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR, input_email)))
    driver.find_element(By.CSS_SELECTOR, input_email).send_keys(file['Login Email'])
    driver.find_element(By.CSS_SELECTOR, input_first_name).send_keys(file['First Name'])
    driver.find_element(By.CSS_SELECTOR, input_last_name).send_keys(file['Last Name'])
    driver.find_element(By.CSS_SELECTOR, input_address).send_keys(file['Address'])
    driver.find_element(By.CSS_SELECTOR, input_city).send_keys(file['City'])
    driver.find_element(By.CSS_SELECTOR, input_zip).send_keys(file['ZipCode'])
    Select(driver.find_element(By.CSS_SELECTOR, input_state)).select_by_visible_text('Colorado')
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, tag_to_payment)))
    driver.find_element(By.CSS_SELECTOR, tag_to_payment).click()
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, tag_to_payment)))
    driver.find_element(By.CSS_SELECTOR, tag_to_payment).click()

    # Payment info input
    shipping = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, same_as_shipping)))
    shipping.click()

    actions = ActionChains(driver)
    actions.move_to_element_with_offset(shipping, 0, -340).click().perform()
    actions.send_keys(file['Card Number']).perform()
    actions.send_keys(Keys.TAB * 2).perform()
    actions.send_keys(f'{file["First Name"]} {file["Last Name"]}').perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(f'{file["Card Expire Month"]} {file["Card Expire Year"]}').perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(file['Card CVV 3 Digits']).perform()

    payment = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, pay_now)))
    payment.click()

    while True:
        pass


if __name__ == '__main__':
    main()
