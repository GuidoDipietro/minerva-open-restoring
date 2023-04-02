from PyPDF2 import PdfReader
import re
import json

DIR = "PDFs"

EVENTS = ["333", "555", "666", "777", "Clock", "Mega", "Pyra", "Skewb"]
GROUPS = "ABC"
ROUNDS = ["R1"]

def clean(string):
    """Clean whitespace, remove trash, strip string"""
    string = re.sub(r'\s+', ' ', string).replace("Extra Scrambles E", "")
    return string.strip()

for event in EVENTS:
    for group in GROUPS:
        for round in ROUNDS:
            # Create PDF reader
            FILENAME = fr"{event}{round}{group}.pdf"
            reader = PdfReader(fr"{DIR}/{FILENAME}")

            # Read text from first and only page
            pageobj = reader.pages[0]
            text = pageobj.extract_text()

            # Hack to then split each scramble
            scraw = text            \
                .replace("1",",")   \
                .replace("\n2",",") \
                .replace("\n3",",") \
                .replace("\n4",",") \
                .replace("\n5",",") \
                .replace("E1",",")  \
                .replace("E2",",")

            # Get first 7 elements which is max we'll need idk why I did this like that (it was 3am)
            scrs = [clean(x) for x in scraw.split(",") if x][:7]

            # Some events have just 3 scrambles not 5
            numscrams = 3 if event in ["666","777"] else 5

            # Generate JSON
            obj = json.dumps({
                "scrambles": scrs[:numscrams],
                "extraScrambles": scrs[numscrams:numscrams+2],
            }, indent=2)

            # Profit
            print(FILENAME, obj, sep="\n", end="\n"+"-"*65+"\n")
