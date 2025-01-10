import requests
from bs4 import BeautifulSoup
import pandas as pd

from openai import OpenAI

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

client = OpenAI()

file_response = client.files.create(
  file=open("films.csv", "rb"),
  purpose="assistants"
)
file_id = file_response.id

assistant = client.beta.assistants.create(
    instructions=("You are an movie recommendation bot, and you have access to the user's movie diary. You can recommend movies based on the user's diary entries."
            "Identify High-Rated Movies: Focus on the movies rated highly. Genres and Directors: If available, look for patterns in genres or directors the user prefers. "
            "Actors and Themes: Consider any recurring actors or themes if the data provides such insights. Variety: Ensure a diverse set of recommendations across different genres and themes."
            "Since the current data only includes titles, years, ratings, and date watched, Focus on these aspects for recommendations. Based on this, Identify potential movies that align with user preferences."
            "Keep the output incredibly concise, in format with no formatting: [Title, Year]. Do not recommend movies that the user has already watched. Ratings are stars out of 5."),
    name="Movie Recommendation Bot",
    tools=[{"type": "code_interpreter"}],
    temperature=0.6,
    model="gpt-4o"
)




print(client.beta.assistants.list())

thread = client.beta.threads.create(
messages=[
  {
    "role": "user",
    "content": ("Using the data from my movie diary (attached file films.csv), can you recommend me 15 movies? "),
    "attachments": [
      {
        "file_id": file_id,
        "tools": [{"type": "code_interpreter"}]
      }
    ]
  }
]
)
print(thread)

run = client.beta.threads.runs.create_and_poll(
    assistant_id=assistant.id,
    thread_id=thread.id
)

# if run.status == 'completed': 
#     messages = client.beta.threads.messages.list(
#         thread_id=thread.id
#     )
#     print(messages)
# else:
#     print(run.status)   
    
messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

if messages.data:
    first_message = messages.data[0]
    print(first_message.role + ": " + first_message.content[0].text.value)