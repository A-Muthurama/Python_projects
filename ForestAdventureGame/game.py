import random

# Game data
def setup_game(name):
    return {
        "name": name,
        "health": 100,
        "gold": 50,
        "items": [],
        "location": "town"
    }

items = {
    "health potion": {"health": 30, "price": 20},
    "sword": {"damage": 10, "price": 50}
}

enemies = [
    {"name": "Goblin", "health": 30, "damage": 5, "gold": 15},
    {"name": "Wolf", "health": 20, "damage": 7, "gold": 10},
    {"name": "Bandit", "health": 40, "damage": 8, "gold": 25}
]

def process_action(player, location, action):
    result = ""
    next_page = location

    if location == "town":
        if action == "shop":
            next_page = "shop"
        elif action == "forest":
            next_page = "forest"
        elif action == "rest":
            if player['gold'] >= 10:
                player['gold'] -= 10
                player['health'] = 100
                result = "You rested and restored full health."
            else:
                result = "Not enough gold to rest."
        elif action == "quit":
            result = "Thanks for playing!"
            next_page = "index"

    elif location == "shop":
        if action == "buy health potion":
            result = buy_item(player, "health potion")
        elif action == "buy sword":
            result = buy_item(player, "sword")
        elif action == "return":
            next_page = "town"

    elif location == "forest":
        if action == "explore":
            encounter = random.choices(["enemy", "treasure", "nothing"], [60, 30, 10])[0]
            if encounter == "enemy":
                result = enemy_encounter(player)
            elif encounter == "treasure":
                result = treasure_encounter(player)
            else:
                result = "You found nothing interesting."
        elif action == "camp":
            player["health"] = min(player["health"] + 10, 100)
            result = "You set up camp and recovered 10 health."
        elif action == "return":
            next_page = "town"

    return result, next_page

def buy_item(player, item_name):
    item = items[item_name]

    if item_name in player["items"] and item_name != "health potion":
        return f"You already have a {item_name}."

    if player["gold"] >= item["price"]:
        player["gold"] -= item["price"]
        if item_name != "health potion":
            player["items"].append(item_name)
        else:
            player["items"].append(item_name)
        return f"You bought a {item_name}!"
    else:
        return "Not enough gold!"

def enemy_encounter(player):
    enemy = random.choice(enemies)
    player_damage = 5 + (items["sword"]["damage"] if "sword" in player["items"] else 0)
    rounds = ""

    while enemy["health"] > 0 and player["health"] > 0:
        enemy["health"] -= player_damage
        rounds += f"You hit {enemy['name']} for {player_damage} damage. "

        if enemy["health"] <= 0:
            player["gold"] += enemy["gold"]
            rounds += f"You defeated {enemy['name']} and got {enemy['gold']} gold!"
            return rounds

        player["health"] -= enemy["damage"]
        rounds += f"{enemy['name']} hit you for {enemy['damage']} damage. "

        if player["health"] <= 0:
            return "You died in battle. Game Over."

    return rounds

def treasure_encounter(player):
    gold = random.randint(10, 30)
    player["gold"] += gold

    if random.random() < 0.2:
        player["items"].append("health potion")
        return f"You found a treasure chest! +{gold} gold and a health potion."
    return f"You found some hidden gold! +{gold} gold."
