from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

from account import check_file
from time import sleep


options = Options()
options.headless = False
driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)

# _website = ''
_website = ''

first_pos_item = '//*[@id="shopify-section-collection-template"]/div[1]/div[1]'

tag_items = 'span.product-item__meta__inner'
tag_title = 'p.product-item__title'
tag_sold_out = 'p.product-item__sold-out'
tag_add_cart = '#AddToCart-product-template'
tag_check_out = '#CartContainer > form > div.ajaxcart__footer.ajaxcart__footer--fixed > button'
tag_to_payment = '#continue_button'

input_email = '#checkout_email'
input_first = '#checkout_shipping_address_first_name'
input_last = '#checkout_shipping_address_last_name'
input_address = '#checkout_shipping_address_address1'
input_city = '#checkout_shipping_address_city'
input_state = '#checkout_shipping_address_province'
input_zip = '#checkout_shipping_address_zip'

input_card = '#number'
input_card_name = '#name'
input_card_exp = '#expiry'
input_card_security = '#verification_value'
same_as_shipping = '#checkout_different_billing_address_false'


def main():
    # item_name = input('What are you searching for? ')
    item_name = 'cash'
    file = check_file()

    print('Started')
    driver.get(_website)
    print('Loading Webpage')

    # Page loading
    running = True
    while running:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, first_pos_item)))
        find_all_product_elements = driver.find_elements(By.CSS_SELECTOR, tag_items)

        for product in find_all_product_elements:
            description = product.get_attribute('innerText')
            print(description[:15] + str(len(find_all_product_elements)))
            if item_name in description:
                if 'Sold Out' not in description:
                    price = description[-4:]
                    title = f'{description[:30]}...'
                    product.click()
                    print(f'{title}  {price}')
                    running = False
                    break

            elif product == find_all_product_elements[-1]:
                print('No item found refreshing')
                sleep(5)
                driver.refresh()

    # Add to cart and goto checkout
    add_cart_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, tag_add_cart)))
    sleep(1)
    add_cart_element.click()
    check_out_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, tag_check_out)))
    sleep(1.5)
    check_out_element.click()

    # Enter Shipping Info
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, input_email)))
    driver.find_element(By.CSS_SELECTOR, input_email).send_keys(file['Login Email'])
    driver.find_element(By.CSS_SELECTOR, input_first).send_keys(file['First Name'])
    driver.find_element(By.CSS_SELECTOR, input_last).send_keys(file['Last Name'])
    driver.find_element(By.CSS_SELECTOR, input_address).send_keys(file['Address'])
    driver.find_element(By.CSS_SELECTOR, input_city).send_keys(file['City'])
    driver.find_element(By.CSS_SELECTOR, input_zip).send_keys(file['ZipCode'])
    Select(driver.find_element(By.CSS_SELECTOR, input_state)).select_by_visible_text('Some where')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, tag_to_payment)))
    driver.find_element(By.CSS_SELECTOR, tag_to_payment).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, tag_to_payment)))
    driver.find_element(By.CSS_SELECTOR, tag_to_payment).click()

    # Payment info input
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, same_as_shipping)))
    driver.find_element(By.CSS_SELECTOR, same_as_shipping).click()
    shipping = driver.find_element(By.CSS_SELECTOR, same_as_shipping)

    actions = ActionChains(driver)
    actions.move_to_element_with_offset(shipping, 0, -340).click().perform()
    actions.send_keys(file['Card Number']).perform()
    actions.send_keys(Keys.TAB * 2).perform()
    actions.send_keys(f'{file["First Name"]} {file["Last Name"]}').perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(f'{file["Card Expire Month"]} {file["Card Expire Year"]}').perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(file['Card CVV 3 Digits']).perform()


if __name__ == '__main__':
    main()
