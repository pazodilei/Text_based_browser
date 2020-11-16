import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore
init(autoreset=True)

args = sys.argv
history = []

if args[1]:
    try:
        os.mkdir(f"./{args[1]}")
    except FileExistsError:
        pass
    while True:
        web_site = input()
        if web_site == "back":
            history.pop()
            if len(history) > 0:
                with open(f"./{args[1]}/{history.pop()}", "r") as f:
                    print(f.read())
        elif web_site == "exit":
            break
        if web_site.startswith("http"):
            pass
        else:
            web_site = "http://" + web_site
        if web_site[7:] in os.listdir(f"./{args[1]}"):
            history.append(web_site[7:])
            with open(f"./{args[1]}/{web_site[7:]}", "r") as f:
                print(f.read())
        elif "." in web_site:
            file_name = web_site[7: web_site.index('.')]
            r = requests.get(web_site)
            history.append(file_name)
            soup = BeautifulSoup(r.content, "html.parser")
            text = ""
            for tag in soup.find_all(["a", "p", "head", "ul", "ol", "li"]):
                if tag.name == "a":
                    text += tag.text.strip() + "\n"
                    print(Fore.BLUE + text)
                text += tag.text.strip() + "\n"
            with open(f"./{args[1]}/{file_name}", "w", encoding="UTF-8") as f:
                f.write(text)
        else:
            print("error in url")
