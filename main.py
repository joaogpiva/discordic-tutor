import requests

random = requests.get("https://api.scryfall.com/cards/random").json()
print("Nome: " + random["name"])
print("Custo de Mana: " + random["mana_cost"])
print("Texto: " + random["oracle_text"])
if "flavor_text" in random:
    print(random["flavor_text"])