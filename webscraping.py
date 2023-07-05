
import requests
from bs4 import BeautifulSoup

# gets the webpage
req = requests.get("https://www.kokr8.com/")

# scrapes page
soup = BeautifulSoup(req.content, "html.parser")
cocreatetext = soup.get_text()

# reformats it
newwords = cocreatetext.replace("\n", "  ")
webscrapelist = newwords.split("  ")

with open("kocreate.csv", "w") as fp:
    for line in webscrapelist:
        filetext = line.format()
        fp.write(filetext)
        print(line)


