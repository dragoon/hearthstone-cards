import json
import requests
CARDS_API_URL = 'https://api.hearthstonejson.com/v1/23180/{}/cards.collectible.json'

main_lang = 'en'
langs = ['fr', 'de', 'ru']

# generate pairs
cards = {}
for card in requests.get(CARDS_API_URL.format("enUS")).json():
    if "name" in card:
        cards[card['dbfId']] = {"main_flavor": card.get("flavor", ""), "main_name": card["name"]}
for lang in langs:
    data = requests.get(CARDS_API_URL.format(lang+lang.upper())).json()
    for card in data:
        if "name" in card:
            cards[card['dbfId']].update({"flavor": card.get("flavor", ""), "name": card["name"]})
    # output CSV
    out = open("anki_cards_{}-{}.tsv".format(main_lang, lang), "w")
    for card in cards.values():
        if card['name'] == card['main_name']:
            continue
        out.write('\t'.join([card['name'], card['main_name']]) + '\n')
    out.close()
