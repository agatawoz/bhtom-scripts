'''
This script allows to get a token for the BHTOM API. It writes the token to a file called "token.txt".

'''


import requests
import getpass

#Login to BHTOM account
print("Log to your BHTOM account:")
username = input("Login: ")
password = getpass.getpass("Password: ")

url = "https://bh-tom2.astrolabs.pl/api/token-auth/"

#Send request
response = requests.post(
    url,
    json={"username": username, "password": password}
)

#Answer handling
if response.status_code == 200:
    token = response.json().get("token")
    print("Your token:", token)

    #Write token to file
    with open("token.txt", "w") as f:
        f.write(token)

else:
    print("Error:", response.status_code)