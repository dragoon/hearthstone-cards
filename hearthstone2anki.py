import json
import argparse
import requests


def extend_lang(lang: str):
    if lang == 'en':
        return 'enUS'
    return lang.lower() + lang.upper()

CARDS_API_URL = 'https://api.hearthstonejson.com/v1/23180/{}/cards.collectible.json'

parser = argparse.ArgumentParser(description='Generate hearthstone card names as language pairs in CSV format.')
parser.add_argument('--from', dest='main_lang', metavar='FROM_LANG', default='en',
                    help='main language to generate language pairs')
parser.add_argument('--to', metavar='TO_LANG', nargs='+', default=['fr'],
                    help='foreign languages to generate language pairs')

args = parser.parse_args()

main_lang = args.main_lang
destination_langs = args.to

# generate pairs
cards = {}
for card in requests.get(CARDS_API_URL.format(extend_lang(main_lang))).json():
    if "name" in card:
        cards[card['dbfId']] = {"main_flavor": card.get("flavor", ""), "main_name": card["name"]}
for lang in destination_langs:
    data = requests.get(CARDS_API_URL.format(extend_lang(lang))).json()
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
