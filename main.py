import requests
import time
import base64
import json
from colorama import Fore, Style

x_super_properties = {
    "os": "Windows",
    "client_build_number": 280472
}

lootbox_items = {
    "1214340999644446723": "👢 Speed Boost",
    "1214340999644446724": '🪈 →↑↓→↑↓',
    "1214340999644446722": '🐢 Wump Shell',
    "1214340999644446728": '🔨 Dream Hammer',
    "1214340999644446725": '⛑️ Power Helmet',
    "1214340999644446726": '🦆 Quack!!',
    "1214340999644446721": '🧸 Cute Plushie',
    "1214340999644446727": '🍌 OHHHHH BANANA',
    "1214340999644446720": '🗡️ Buster Blade',

}

unlocked_items = []

def has_found_all():
    return len(unlocked_items) >= 9

invalidToken = True

while invalidToken:

    token = input(f"{Fore.GREEN}[🔑] Paste your Discord token: {Style.RESET_ALL}")

    headers = {
        "x-super-properties": base64.b64encode(json.dumps(x_super_properties).encode('utf-8')).decode('utf-8'),
        "referrer": "https://discord.com/channels/@me",
        "authorization": token,
    }

    response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

    if response.status_code == 200:
        invalidToken = False
    elif response.status_code == 401:
        print(f"{Fore.RED}[⚠️] Invalid token! Try again...{Style.RESET_ALL}")


print(f"\n{Fore.GREEN}[👤] Logged in as: {Fore.MAGENTA}{response.json()['username']}{Style.RESET_ALL}\n")

response = requests.get("https://discord.com/api/v9/users/@me/lootboxes", headers=headers)

data = response.json()

for item in data['opened_items']:
    unlocked_items.append(item)

prizeUnlocked = has_found_all()

while not prizeUnlocked:

    response = requests.post("https://discord.com/api/v9/users/@me/lootboxes/open", headers=headers)

    data = response.json()

    if data["opened_item"] not in unlocked_items:
        print(f"{Fore.GREEN}[🎁] Unlocked a NEW lootbox item: {Fore.MAGENTA}{lootbox_items[data['opened_item']]}{Style.RESET_ALL}")
        unlocked_items.append(data["opened_item"])
    else:
        print(f"{Fore.RED}[🎁] Found an old lootbox item: {Fore.MAGENTA}{lootbox_items[data['opened_item']]}{Style.RESET_ALL}")

    time.sleep(5)

    prizeUnlocked = has_found_all()

print(f"{Fore.YELLOW}[🎉] You have unlocked all 9 available items and won the final prize!{Style.RESET_ALL}")

response = requests.get("https://discord.com/api/v9/users/@me/lootboxes", headers=headers)

data = response.json()

if not data["redeemed_prize"]:
    response = requests.post("https://discord.com/api/v9/users/@me/lootboxes/redeem-prize", headers=headers)
    if response.json()["redeemed_prize"]:
        print(f'[🤡] Automatically redeemed reward: "I\'m a Clown" Avatar Decoration')

print(f"\n{Fore.CYAN}[📈] Statistics{Style.RESET_ALL}")

opened_items = data['opened_items']

for key, value in opened_items.items():
    lootbox_item = lootbox_items[key]
    print(f"{Style.BRIGHT}{lootbox_item}{Style.RESET_ALL}: {value} found")

total = sum(list(opened_items.values()))
print(f"{Style.BRIGHT}Total{Style.RESET_ALL}: {total} items found\n")