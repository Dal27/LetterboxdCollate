import requests
from bs4 import BeautifulSoup
import pandas as pd

from openai import OpenAI

import httpx
import asyncio

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List




app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FilmRecommendation(BaseModel):
  title: str
  year: str

class UserRequest(BaseModel):
    username: str

async def fetch_page(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

async def scrape_movies(username):
  data = []
  current_page = 1
  proceed = True

  while(proceed):
      
      url = "https://letterboxd.com/"+str(username)+"/films/diary/page/"+str(current_page)+"/"
      page = requests.get(url)
      soup = BeautifulSoup(page.text, "html.parser")


      if not soup.find_all("tr", class_="diary-entry-row"):
          proceed = False
      else:
          # print("Currently Scraping page: "+str(current_page))
          
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
  return "films.csv"


async def get_recommendations_from_openai(file_path):
  client = OpenAI()

  file_response = client.files.create(
    file=open(file_path, "rb"),
    purpose="assistants"
  )
  file_id = file_response.id

  assistant = client.beta.assistants.create(
      instructions=(
          "You are a movie recommendation bot, and you have access to the user's movie diary. "
          "You can recommend movies based on the user's diary entries. "
          "Focus on the movies rated highly. If available, look for patterns in genres or directors the user prefers. "
          "Consider any recurring actors or themes if the data provides such insights. Ratings are stars out of 5. "
          "Since the current data only includes titles, years, ratings, and date watched, focus on these aspects for recommendations. "
          "Identify potential movies that align with user preferences. "
          "Keep the output incredibly concise, in the format: [Title, Year] (no formatting or numbering). "
          "Double-check to see if a recommended movie is in the movie diary, if so remove the recommendation."
      ),
      name="Movie Recommendation Bot",
      tools=[{"type": "code_interpreter"}],
      temperature=0.8,
      model="gpt-4o"
  )

  # print(client.beta.assistants.list())

  thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": ("Using the data from my movie diary (attached file films.csv), can you recommend me 15 movies? "
                  "Do not include any introductory phrases like 'Based on your highly-rated movies here are 15 movie recommendations' and do not include numbering of the films."),
      "attachments": [
        {
          "file_id": file_id,
          "tools": [{"type": "code_interpreter"}]
        }
      ]
    }
  ]
  )
  # print(thread)

  run = client.beta.threads.runs.create_and_poll(
      assistant_id=assistant.id,
      thread_id=thread.id
  )

  messages = client.beta.threads.messages.list(
          thread_id=thread.id
      )

  try:
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    if messages.data:
      first_message = messages.data[0]
      recommendations = first_message.content[0].text.value.split("\n")
      films = []
      for rec in recommendations:
        if rec:
          title, year = rec.split(", ")
          films.append(FilmRecommendation(title=title, year=year))
      return films
    else:
      raise HTTPException(status_code=404, detail="No recommendations found")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
  

@app.post("/scrape_and_recommend", response_model=List[FilmRecommendation])
async def scrape_and_recommend(request: UserRequest):
    try:
        file_path = await scrape_movies(request.username)
        recommendations = await get_recommendations_from_openai(file_path)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)