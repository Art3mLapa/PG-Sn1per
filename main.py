import random
import requests
import time
import os
from colorama import Fore, Style

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def menu():
    print(Fore.RED + '''
______ _____    _____       __                  
| ___ \  __ \  /  ___|     /  |                 
| |_/ / |  \/  \ `--. _ __ `| | _ __   ___ _ __ 
|  __/| | __    `--. \ '_ \ | || '_ \ / _ \ '__|
| |   | |_\ \  /\__/ / | | || || |_) |  __/ |_  
\_|    \____/  \____/|_| |_\___/ .__/ \___|_(_) 
                               | |              
                               |_|              1.0 by Art3mLapa.
                ''' + Style.RESET_ALL)

def generate_random_number(min_length, max_length):
    length = random.randint(min_length, max_length)
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def check_profile_link(profile_url, random_number):
    response = requests.get(profile_url)
    if response.url == "https://www.roblox.com/request-error?code=404":
        print(f"[X] Account not exist:{random_number}")
        return False
    else:
        return True

def check_inventory_link(inventory_url, random_number):
    response = requests.get(inventory_url)
    data = response.json()
    if not data:
        print(f"[X] Account dont have item:{random_number}")
    return data

def generate_and_check_links():
    with open("webhook.txt", "r") as file:
        webhook_url = file.read().strip()

    while True:
        clear_console()
        menu()
        itemID = input(Fore.YELLOW + "Item(ID) > ")
        random_number = generate_random_number(7, 8) # minimum, maximum ID length
        profile_url = f"https://www.roblox.com/users/{random_number}/profile"
        if not check_profile_link(profile_url, random_number):
            continue
        
        inventory_url = f"https://inventory.roblox.com/v1/users/{random_number}/items/0/{itemID}/is-owned"
        if not check_inventory_link(inventory_url, random_number):
            continue

        webhook_data = {
            "content": "Account Sniped!",
            "embeds": [
                {
                    "title": random_number,
                    "url": profile_url,
                    "description": "PG Sniper webhook"
                }
            ]
        }
        response = requests.post(webhook_url, json=webhook_data)
        if response.status_code == 204:
            print(f"[!] Success! {random_number}")
        else:
            print("[X] Failed to send webhook")

generate_and_check_links()
