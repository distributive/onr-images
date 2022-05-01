from bs4 import BeautifulSoup
import json
import re
import unidecode
import urllib.request

################################################################################

file = "cards.json"

pages = [
    "https://www.emergencyshutdown.net/webminster/sets/base",
    "https://www.emergencyshutdown.net/webminster/sets/classic",
    "https://www.emergencyshutdown.net/webminster/sets/proteus"
    ]

################################################################################

def main():
    cards = []
    for page in pages:
        soup = BeautifulSoup(urllib.request.urlopen(page).read(), 'html.parser')
        for card_html in soup.find_all(class_="panel-primary"):
            card = {}
            card["title"] = card_html.h3.text
            card["stripped_title"] = strip_text(card["title"])
            card["code"] = to_code(card["title"])
            labels = card_html.find_all("label")
            values = card_html.find_all("span")
            for i in range(len(labels)):
                label = labels[i].text[:-2].lower()
                value = values[i].text.replace("\r", "")
                if label == "side":
                    card["side"] = value
                elif label == "type":
                    card["type"] = value
                elif label == "subtypes":
                    card["subtypes"] = value.split(" - ")
                elif label == "set":
                    card["set"] = value
                    card["set_code"] = to_code(value)
                elif label == "rarity":
                    card["rarity"] = value
                elif label == "cost":
                    card["cost"] = value
                elif label == "strength":
                    card["strength"] = value
                elif label == "difficulty":
                    card["difficulty"] = value
                elif label == "agenda points":
                    card["agenda_points"] = value
                elif label == "text":
                    card["text"] = value
                    card["stripped_text"] = strip_text(value)
                elif label == "artist":
                    card["artist"] = value
            card["image"] = "http://www.emergencyshutdown.net/images/onr/" + card["set_code"] + "/" + card["code"] + ".jpg"
            cards.append(card)
            print(card["image"])
    json_object = json.dumps(cards, indent=4)

    f = open(file, "w")
    f.write(json_object)
    f.close()

    print("Data saved in " + file)

################################################################################

r_space = re.compile(r" +")
r_bits = re.compile(r"\[(\d+)\]")
r_brackets = re.compile(r"\((.*?)\)")
r_square = re.compile(r"\[(.*?)\]")
r_noncode = re.compile(r"\.|,|!|'")

def strip_text(t):
    t = unidecode.unidecode(t)
    t = t.replace("\n", " ")
    t = t.replace('\"', "")
    t = r_space.sub(" ", t)
    t = t.replace("[T]", "trash")
    t = t.replace("[T]", "subroutine: ")
    t = t.replace("[1]", "1 bit")
    t = r_bits.sub(r"\1 bits", t)
    return t

def to_code(title):
    t = strip_text(title.lower())
    t = r_noncode.sub("", t)
    t = r_brackets.sub("", t)
    t = r_square.sub("", t)
    t = r_space.sub("_", t)
    return t

################################################################################

if __name__ == "__main__":
    main()
