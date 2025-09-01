'''
This script allows to get a token for the BHTOM API. 

'''

import requests
import argparse

url = "https://bh-tom2.astrolabs.pl/api/token-auth/"


def main():
    
    parser = argparse.ArgumentParser("Login to your BHTOM account")
    parser.add_argument('--login', default=None, help='Your BHTOM login')
    parser.add_argument('--password', default=None, help='Your BHTOM password')

    args = parser.parse_args()
    login = args.login
    password = args.password


    #send request
    response = requests.post(
        url,
        json={"username": login, "password": password}
    )

    #answer handling
    if response.status_code == 200:
        token = response.json().get("token")
        print("Your token:", token)
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    main()