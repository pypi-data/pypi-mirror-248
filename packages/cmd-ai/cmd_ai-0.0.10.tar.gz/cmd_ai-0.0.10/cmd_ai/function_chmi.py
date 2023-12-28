#!/usr/bin/env python3

from cmd_ai import config
from cmd_ai.version import __version__
import json

"""
You are an assistant in Czech language, your responses are brief, you dont repeat users input. You can interpret weather situation or prediction in Czech Republic with the only interest in central Bohemia.

##
{
  "name": "get_weather",
  "description": "Determine weather or weather prediction in Czech Republic ",
  "parameters": {
    "type": "object",
    "properties": {
      "time": {
        "type": "string",
        "description": "today, tomorrow"
      }
    },
    "required": [
      "time"
    ]
  }
}

#### return json

{"weather":" Počasí přes den (07-24): > Zpočátku skoro jasno až polojasno, zejména na Moravě a severovýchodě Čech místy mlhy, i mrznoucí. Postupně od severozápadu přibývání oblačnosti a později v severozápadní polovině území místy déšť, i mrznoucí, a nad 1000 m i sněžení. Nejvyšší teploty 6 až 10 °C, při slabém větru kolem 4 °C, zejména na střední Moravě a severovýchodě Čech, v 1000 m na horách kolem 5 °C. Mírný jihozápadní až západní vítr 3 až 7 m/s, místy s nárazy kolem 15 m/s. Zejména na severovýchodě Čech a na Moravě vítr jen slabý proměnlivý do 3 m/s."}

"""


from fire import Fire
import datetime as dt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from subprocess import getoutput

from console import fg

def get_chmi(time, url="https://www.chmi.cz/predpovedi/predpovedi-pocasi/ceska-republika/predpoved-na-dnesek-resp-zitra"):
    res = "No information about weather is available now."
    if time not in ["today","tomorrow"]:
        return json.dumps(  {"weather":res } , ensure_ascii=False)  # MUST OUTPUT FORMAT



    options = Options()
    #firefox_options = FirefoxOptions()
    #firefox_options.add_argument("--headless")  # Run in headless mode


    options.binary_location = getoutput("find /snap/firefox -name firefox").split("\n")[-1]
    options.add_argument("--headless")  # Run in headless mode

    driver = webdriver.Firefox(service = Service(executable_path = getoutput("find /snap/firefox -name geckodriver").split("\n")[-1]),    options = options)
    #url = 'https://cnn.com'
    driver.get(url)

    # Fetch the webpage
    #print("D... getting")
    driver.get(url)

    #print(" Get the page source and close the browser")
    page_source = driver.page_source
    driver.quit()

    #print("# Parse the page source with BeautifulSoup")
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the desired heading
    heading = soup.find('p', class_='nadpis')
    heading_text = heading.get_text(strip=True) if heading else 'Heading not found'

    # Find all the paragraphs with the specified class and extract their text
    #paragraphs = soup.find_all


    hierarchy = {}
    current_header = None
    current_sub = None
    numb=0

    for p in soup.find_all('p',class_=['podnadpis','textik1','textik2']):
        if "podnadpis" in p['class']:
            numb+=1
            current_header = p.get_text()
            current_header = f"N{numb} {current_header}"
            hierarchy[current_header] = {}
        elif 'textik1' in p['class'] or 'textik2' in p['class']:
            if current_header:
                # Add text to the current header section
                line = p.get_text()
                if 'textik1' in p['class']:
                    line = f"{line}"
                    current_sub = p.get_text()
                    current_sub = f"{current_sub}"
                    hierarchy[current_header][current_sub]=[]
                if 'textik2' in p['class']:
                    line = f"{line}"
                    line = line.replace(r'\xa0','')
                    if current_sub:
                        hierarchy[current_header][current_sub].append( line)

    # I have all:
    WDT = dt.datetime.now().strftime("%A")
    WDM = (dt.datetime.now()+dt.timedelta(days=1)).strftime("%A")
    WDd = {
        "Monday": "pondělí",
        "Tuesday": "úterý",
        "Wednesday": "středu",
        "Thursday": "čtvrtek",
        "Friday": "pátek",
        "Saturday": "sobotu",
        "Sunday": "neděli"
    }


    #print("Today is : ", WDT, WDd[WDT] )
    situace = []
    for i,v in hierarchy.items():
        #print(i)
        for j in list(v.keys()):
            if j == "Tlaková tendence:" or j== "Rozptylové podmínky:":
                del v[j]
            if j == "Situace:" :
                situace.append( "".join(v[j])  ) # list with one element.
                del v[j]
            #print(j):

    situace =     "".join(situace)
    print()
    print( situace )
    print()


    # paragraphs = [p.get_text() for p in soup.find_all('p', class_=['podnadpis','textik1','textik2'])]

    DEMANDED = {}

    for i,v in hierarchy.items():
        print(i, end=" ")
        if i.find("Předpověď")>=0:
            if i.find(WDd[WDT])>=0:
                print(f" {fg.red}TODAY{fg.default} ")
                if time == "today":
                    DEMANDED = v
            elif i.find(WDd[WDM])>=0:
                print(f"{fg.red} TOMORROW {fg.default} ")
                if time == "tomorrow":
                    DEMANDED = v
            else:
                print()
        else:
            print()


        for j,w in v.items():
            print("  ",j)
            for k in w:
                #print(i.decode('utf8') )# subst(r'\xa0','') )
                print("  > ",k )#.replace(r'\xa0','') )




    if len(DEMANDED)>0:
        res = []
        for i,v in DEMANDED.items():
            for j in v:
                res.append(j)
        res = "".join(res)
    # Formulate output
    return json.dumps(  {"weather":res } , ensure_ascii=False)  # MUST OUTPUT FORMAT


if __name__=="__main__":
    Fire(get_chmi)
