import requests
from bs4 import BeautifulSoup
import pandas as pd

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates




# app = FastAPI()

# origins = [
#     "http://localhost",
#     "https://localhost",
#     "http://localhost:3000",
#     "https://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


data = []
current_page = 1
proceed = True

while(proceed):
    
    url = "https://letterboxd.com/dal27/films/diary/page/"+str(current_page)+"/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")


    if not soup.find_all("tr", class_="diary-entry-row"):
        proceed = False
    else:
        print("Currently Scraping page: "+str(current_page))
        
        table = soup.find("table", id="diary-table")
        for row in table.find_all("tr", class_="diary-entry-row"):
            film = {}
            film['title'] = row.find("h3", class_="headline-3 prettify").text.strip()
            film['year'] = row.find("td", class_="td-released center").text.strip()
            film['rating'] = row.find("span", class_="rating").text.strip()
            date_tag = row.find("td", class_="td-day diary-day center").find("a")
            film['date_watched'] = date_tag['href'].split('/')[-4] + '/' + date_tag['href'].split('/')[-3] + '/' + date_tag['href'].split('/')[-2]
            
            data.append(film)
        current_page += 1
        
df = pd.DataFrame(data)
df.to_csv("films.csv")
