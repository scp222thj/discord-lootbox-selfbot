import requests
import time
import base64
import json
from colorama import Fore, Style

API_URL = "https://discord.com/api/v9"

class LootboxBot:
    LOOTBOX_ITEMS = {
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

    def __init__(self, token):
        self.headers = get_headers(token)

    def open_lootbox(self):
        response = requests.post(f"{API_URL}/users/@me/lootboxes/open", headers=self.headers)

        data = response.json()

        if data["opened_item"] not in self.unlocked_items:
            print(f"{Fore.GREEN}[🎁] Unlocked a NEW lootbox item: {Fore.MAGENTA}{self.LOOTBOX_ITEMS[data['opened_item']]}{Style.RESET_ALL}")
            self.unlocked_items.append(data["opened_item"])
        else:
            print(f"{Fore.RED}[🎁] Found an old lootbox item: {Fore.MAGENTA}{self.LOOTBOX_ITEMS[data['opened_item']]}{Style.RESET_ALL}")

        time.sleep(5)

    def redeem_prize(self):
        response = requests.post(f"{API_URL}/users/@me/lootboxes/redeem-prize", headers=self.headers)
        if response.json()["redeemed_prize"]:
            print(f'[🤡] Automatically redeemed reward: "I\'m a Clown" Avatar Decoration')

    def log_stats(self, items):
        print(f"\n{Fore.CYAN}[📈] Statistics{Style.RESET_ALL}")

        for key, value in items.items():
            lootbox_item = self.LOOTBOX_ITEMS[key]
            print(f"{Style.BRIGHT}{lootbox_item}{Style.RESET_ALL}: {value} found")

        total = sum(list(items.values()))
        print(f"{Style.BRIGHT}Total{Style.RESET_ALL}: {total} items found\n")

    def run(self):
        response = requests.get(f"{API_URL}/users/@me/lootboxes", headers=self.headers)

        data = response.json()

        for item in data['opened_items']:
            self.unlocked_items.append(item)

        while not len(self.unlocked_items) >= len(self.LOOTBOX_ITEMS):
            self.open_lootbox()

        print(f"{Fore.YELLOW}[🎉] You have unlocked all 9 available items and won the final prize!{Style.RESET_ALL}")

        response = requests.get(f"{API_URL}/users/@me/lootboxes", headers=self.headers)

        data = response.json()

        if not data["redeemed_prize"]:
            self.redeem_prize()
        
        self.log_stats(data['opened_items'])

def get_headers(token):
    x_super_properties = {
        "os": "Windows",
        "client_build_number": 280472
    }

    encoded_properties = base64.b64encode(json.dumps(x_super_properties).encode('utf-8')).decode('utf-8')

    return {
        "x-super-properties": encoded_properties,
        "referrer": "https://discord.com/channels/@me",
        "authorization": token,
    }

def main():
    valid_token = False

    while not valid_token:

        token = input(f"{Fore.GREEN}[🔑] Paste your Discord token: {Style.RESET_ALL}")

        response = requests.get(f"{API_URL}/users/@me", headers=get_headers(token))

        if response.status_code == 200:
            valid_token = True
        elif response.status_code == 401:
            print(f"{Fore.RED}[⚠️] Invalid token! Try again...{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}[👤] Logged in as: {Fore.MAGENTA}{response.json()['username']}{Style.RESET_ALL}\n")
    bot = LootboxBot(token)
    bot.run()

if __name__ == "__main__":
    main()