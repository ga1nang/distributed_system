import requests
import time
import random
import configparser
from Blockchain.Backend.core.database.database import AccountDB

fromAccount = "1LYgXwYXw16GJXgDwHV7aCNijnQWYEdc1C"

""" Read all the accounts """
AllAccounts = AccountDB().read()

config = configparser.ConfigParser()
config.read('config.ini')

# Get the Webhost details
webhost = config['Webhost']['host']
webport = config['Webhost']['port']
url = f"http://{webhost}:{webport}/wallet"

def autoBroadcast():
    while True:
        for account in AllAccounts:
            if account["PublicAddress"] != fromAccount:
                paras = {"fromAddress": fromAccount,
                        "toAddress": account["PublicAddress"],
                        "Amount": random.randint(1,35)}

                res = requests.post(url, data = paras)   
        time.sleep(2)