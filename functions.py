import requests

URL = "https://api.scryfall.com/"

def printSimple(card):
    result = ""
    result += card["name"] + " - " + card["mana_cost"] + "\n\n"
    result += card["type_line"] + "\n\n"
    result += card["oracle_text"] + "\n\n"
    if "power" in card:
        if card["power"] == "*":
            result += "\\" + card["power"] + "/"
        else:
            result += card["power"] + "/"
        if card["toughness"] == "*":
            result += "\\" + card["toughness"] + "\n\n"
        else:
            result += card["toughness"] + "\n\n"
    if "loyalty" in card:
        result += "Starting loyalty: " + card["loyalty"] + "\n\n"
    if "flavor_text" in card:
        result += "_" + card["flavor_text"] + "_\n\n"
    
    return result

def getRandomCard():
    isToken = True
    while(isToken):
        card = requests.get(URL + "cards/random")
        if (not card.json()["layout"] == "token") or (not card["layout"].json() == "double_faced_token"):
            isToken = False

    return card.json()

def fuzzySearch(name):
    name = name.replace(" ", "+")
    # TODO: sanitizar direito a pesquisa
    print(URL + "cards/named?fuzzy=" + name)
    card = requests.get(URL + "cards/named?fuzzy=" + name)
    print(card.status_code)
    if card.status_code == 404:
        raise Exception("Card not found, check your spelling and try again.")
        return 

    return card.json()