import random
import requests
import time

def generate_random_number(min_length, max_length):
    length = random.randint(min_length, max_length)
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def get_item_name(item_id):
    if len(item_id) == 3:
       url = f"https://www.roblox.com/bundles/{item_id}"
    else:
       url = f"https://www.roblox.com/items/{item_id}"   
       
    response = requests.get(url)
    redirected_url = response.url
    text_after_dash = redirected_url.split("/")[-1]
    item_name = text_after_dash.replace("-", " ")
    return item_name

def check_inventory_link(inventory_url, random_number):
    response = requests.get(inventory_url)
    data = response.json()
    if not data:
        print(f"[X] Account dont have item:{random_number}")
    return data

def check_profile_link(profile_url, random_number):
    response = requests.get(profile_url)
    if response.url == "https://www.roblox.com/request-error?code=404":
        print(f"[X] Account not exist:{random_number}")
        return False
    else:
        return True


def generate_and_check_links():
    with open("webhook.txt", "r") as file:
        webhook_url = file.read().strip()
        itemID = input("[#] Item(ID) > ")
        item_name = get_item_name(itemID)
        print(f"[!] Item for sniping: {item_name}")
        age = int(input("[#] Age account (2005-2016) > "))
        if age < 2005 or age > 2016:
            print("[X] Incorrent age")
            return
        
        if age == 2005:
            min_length = 2
            max_length = 3
        elif age == 2006:
            min_length = 3
            max_length = 3
        elif age == 2007:
            min_length = 4
            max_length = 4
        elif age == 2008:
            min_length = 5
            max_length = 5
        elif age == 2009:
            min_length = 5
            max_length = 6
        elif age == 2010:
            min_length = 6
            max_length = 6
        elif age == 2011:
            min_length = 6
            max_length = 7
        elif age == 2012:
            min_length = 7
            max_length = 8
        elif age == 2013:
            min_length = 8
            max_length = 9
        elif age == 2014:
            min_length = 9
            max_length = 9
        elif age == 2015:
            min_length = 9
            max_length = 9
        elif age == 2016:
            min_length = 9
            max_length = 10
            
    while True:
        random_number = generate_random_number(min_length, max_length)
        profile_url = f"https://www.roblox.com/users/{random_number}/profile"
        if not check_profile_link(profile_url, random_number):
            continue
        
        if len(itemID) == 3:
            inventory_url = f"https://inventory.roblox.com/v1/users/{random_number}/items/3/{itemID}/is-owned"
        else:
            inventory_url = f"https://inventory.roblox.com/v1/users/{random_number}/items/0/{itemID}/is-owned"
            
        if not check_inventory_link(inventory_url, random_number):
            continue

        return inventory_url

        webhook_data = {
            "content": f"Account Sniped! Item:**{item_name}** {profile_url}"
        }
        
        response = requests.post(webhook_url, json=webhook_data)
        if response.status_code == 204:
            print(f"[!] Success! {random_number}")
        else:
            print("[X] Failed to send webhook")

generate_and_check_links()
