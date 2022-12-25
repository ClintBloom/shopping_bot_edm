import json
import os


_info_file = {
    'First Name': '',
    'Last Name': '',
    'Login Email': '',
    'Login Pass': '',
    'Address': '',
    'ZipCode': '',
    'City': '',

    'Card Number': '',
    'Card Expire Month': '',
    'Card Expire Year': '',
    'Card CVV 3 Digits': '',
}


def check_file():
    if os.path.exists('account.txt'):
        filename = open('account.txt', 'r').read()
        print('Account.txt Exists!, Ensure you have edited this file!')
        filename = json.loads(filename)
    else:
        filename = open('account.txt', 'w')
        print('Account.txt has been created!')
        json.dump(_info_file, filename, indent=1)
        input('Exit program and edit account.txt before continuing')
        quit()
    return filename
