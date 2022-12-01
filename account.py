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
        print('{} Exists!, Ensure you have edited this file!'.format('account.txt'))
        filename = json.loads(filename)
    else:
        filename = open('account.txt', 'w')
        print('{} has been created!'.format('account.txt'))
        json.dump(_info_file, filename, indent=1)
        print('Exit program and edit {} before continuing'.format('account.txt'))
        quit()
    return filename
