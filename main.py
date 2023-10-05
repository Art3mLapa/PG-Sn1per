import random
import requests
import time
import json

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
        print(f"[X] Account doesn't have item: {random_number}")
    
    return data
    
def check_profile_link(profile_url, random_number):
 
    response = requests.get(profile_url)
    
    if response.url == "https://www.roblox.com/request-error?code=404":
        print(f"[X] Account does not exist: {random_number}")
        return False
    else:
        return True
        
def get_thumbnail_url(profile_url):
    url = f'https://thumbnails.roblox.com/v1/users/avatar?userIds={profile_url}&size=250x250&format=Png&isCircular=true'
    
    response = requests.get(url)  
    data = response.json()
    thumbnail_url = data['data'][0]['imageUrl']
    
    return thumbnail_url
    
def get_item_thumbnail(itemID):

    if len(itemID) == 3:
        url = f"https://thumbnails.roblox.com/v1/bundles/thumbnails?bundleIds={itemID}&size=150x150&format=Png&isCircular=false"
    else:
        url = f"https://thumbnails.roblox.com/v1/assets?assetIds={itemID}&returnPolicy=PlaceHolder&size=75x75&format=Png&isCircular=false"
    response = requests.get(url)
    data = response.json()
    item_thumbnail = data['data'][0]['imageUrl']
    return item_thumbnail
    
def get_last_online_date(random_number):
    url = "https://presence.roblox.com/v1/presence/last-online"
    payload = {
        "userIds": [
            random_number
        ]
    }


    while True:
        response = requests.post(url, json=payload)
            
        if response.status_code == 429:
            time.sleep(1)
        else:
            break
        
    data = response.json()
    last_online = data['lastOnlineTimestamps'][0]['lastOnline']
    date = last_online[:10]

    year, month, day = date.split('-')
    formatted_date = f"{year}-{month}-{day}"

    return formatted_date

def get_user_name(random_number):
    url = f"https://users.roblox.com/v1/users/{random_number}"
    response = requests.get(url)
    data = response.json()

    name = data["name"]

    return name
    
def process_data(random_number):
    can_view_inventory_url = f"https://inventory.roblox.com/v1/users/{random_number}/can-view-inventory"
    try:
        response = requests.get(can_view_inventory_url).json()
        can_view = response.get("canView", True)

        if can_view:
            collectibles_url = f"https://inventory.roblox.com/v1/users/{random_number}/assets/collectibles?assetType=8&limit=10&sortOrder=Asc"
            response = requests.get(collectibles_url).json()
            data = response.get("data", [])

            rap_total = sum(item["recentAveragePrice"] for item in data)
            if rap_total > 1000:
                rap_total = str(rap_total)[:-3] + "k"

            limiteds_str = ", ".join(item["name"] for item in data)

            return rap_total, limiteds_str

    except requests.exceptions.RequestException:
        pass

    return None, None

def get_followers(random_number):
    url = f"https://friends.roblox.com/v1/users/{random_number}/followers/count"
    
    response = requests.get(url)
    data = response.json()
    count = data["count"]
    
    return count
    
def get_friends(random_number):
    url = f"https://friends.roblox.com/v1/users/{random_number}/friends/count"
    

    response = requests.get(url)
    data = response.json()
    friends = data["count"]
    
    return friends

def generate_and_check_links():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    
        webhook_url = config['webhook']
        account_age = config['account_age (2005-2016)']
        itemId = config['ItemID']
        follower_limit = config['follower_limit']

        print('''
        ______ _____       _____ _   _  __  ______ ___________   
        | ___ \  __ \     /  ___| \ | |/  | | ___ \  ___| ___ \  
        | |_/ / |  \/_____\ `--.|  \| |`| | | |_/ / |__ | |_/ /  
        |  __/| | _|______|`--. \ . ` | | | |  __/|  __||    /   
        | |   | |_\ \     /\__/ / |\  |_| |_| |   | |___| |\ \ _ 
        \_|    \____/     \____/\_| \_/\___/\_|   \____/\_| \_(_)
                                                         
        by art3mlapa.                                        4.0 VER.''')
        itemID = itemId
        item_name = get_item_name(itemID)
        print(f"[!] Item for sniping: {item_name}")
        age = account_age
        print(f"[!] Account age: {account_age}")
        if age < 2005 or age > 2016:
            print("[X] Incorrent age. Change config")
        
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
                    
        print(f"[!] Follower Limit: {follower_limit}")
        
    while True:
        random_number = generate_random_number(min_length, max_length)
        profile_url = f"https://www.roblox.com/users/{random_number}/profile"
        if not check_profile_link(profile_url, random_number):
            continue
            
        followers = get_followers(random_number)
        if follower_limit != 0 and followers > follower_limit:
            print(f"[X] Too many followers ({followers} > {follower_limit}). {random_number}")
            continue
    
        if len(itemID) == 3:
            inventory_url = f"https://inventory.roblox.com/v1/users/{random_number}/items/3/{itemID}/is-owned"
        else:
            inventory_url = f"https://inventory.roblox.com/v1/users/{random_number}/items/0/{itemID}/is-owned"
        
        if not check_inventory_link(inventory_url, random_number):
            continue
        
        thumbnail_url = get_thumbnail_url(random_number)
        item_thumbnail = get_item_thumbnail(itemID)
        formatted_date = get_last_online_date(random_number)
        name = get_user_name(random_number)
        friends = get_friends(random_number)
        rap, limiteds_str = process_data(random_number)
        
        webhook_data = {
            "content": "",
            "tts": False,
            "embeds": [
                {
                    "id": 871818255,
                    "description": f"=============INFORMATION============\n|<:offsale:1156971012139782154> Nickname :**{name}**\n|<:offsale2:1156971166444032090> Profile **{profile_url}**\n|<:legit:1156971071342391316> Item :**{item_name}**\n|<:egg2014:1156971131203502131> Last Online :**{formatted_date}**\n|<:visor:1156968969027198997> Followers :**{followers}**\n|<:offsale3:1156978510234132500> Friends :**{friends}**\n========INVENTORY INFORMATION========\n|<:robux:1156968214438350858> RAP :**{rap}**\n|<:limited:1156968639010967622> Other Limiteds : **{limiteds_str}**",
                    "fields": [],
                    "title": "Account Sniped!",
                    "color": 65325,
                    "image": {
                        "url": (thumbnail_url)
                    },
                    "footer": {
                        "text": "https://github.com/Art3mLapa/PG-Sn1per. Best free PG roblox scrapper."
                    },
                    "thumbnail": {
                        "url": (item_thumbnail)
                    }
                }
            ],
            "components": [],
            "actions": {}
        }
        response = requests.post(webhook_url, json=webhook_data)
        if response.status_code == 204:
            print(f"[!] Success! {random_number}")
        else:
            print(f"[X] Failed to send webhook {random_number}")

generate_and_check_links()
