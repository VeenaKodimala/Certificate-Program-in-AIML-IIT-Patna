import requests
from datetime import datetime
import os
import json

CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}


def getcategory(title):
    title=title.lower()
    for category, keywords in CATEGORIES.items():
        for word in keywords:
            for word in title:
                return category
    return None

def fetchStories(storyIds):
    try:
        headers = {"User-Agent": "TrendPulse/1.0"}
        collected = []
        category_count = {cat: 0 for cat in CATEGORIES}
        for storyID in storyIds:            
            storyFetchurl = f"https://hacker-news.firebaseio.com/v0/item/{storyID}.json"
            storyJSON = requests.get(storyFetchurl, headers=headers).json()
            if not storyJSON or "title" not in storyJSON:
                continue
            title = storyJSON.get("title")
            #print(f"storyJSON title: {title}")
            category = getcategory(title=title)
            #print(f"category: {category}")
            if category and category_count[category] < 25:
                story = {
                    "post_id": storyJSON.get("id"),
                    "title": title,
                    "category": category,
                    "score": storyJSON.get("score"),
                    "num_comments": storyJSON.get("descendants"),
                    "author": storyJSON.get("by"),
                    "collected_at": datetime.now().strftime("%d-%m-%Y %H:%M"),
                }
                #print(f"story: {story}")
                collected.append(story)
                #print(f"collected: {collected}")
                category_count[category] += 1
                #print(f"category_count: {category_count}")
                print(f"entry added in collected: {category_count}")

                # Checking if all the values in category_count dict is <=25, so that we can break the loop. Since we only need 25 stories per category out of the fetched 500.
                
            if all(value == 25 for value in category_count):
                break
        print(f"category_count: {category_count}")    
        print(f"collectedData: {collected}")    
        return collected        
    except Exception as e:
        print(f"Exception in fetchStories:: {e}")                    

def savetoJSON(data):
    folder=r"D:\Veena\Certificate Program in Artificial Intelligence and Machine Learning\Certificate-Program-in-AIML-IIT-Patna\MODULE 1 - FOUNDATIONS OF DATA\Module1 - MiniProject - Trend Pulse\data"
    os.makedirs(folder,exist_ok=True)
    #This line will concatinate the folder and the filname part. This is better instead of long lines of paths.
    fileName = os.path.join(folder,f"trendingStories_{datetime.now().strftime("%d%m%Y")}.json")
    with open(fileName,"w") as pointer:
        json.dump(data,pointer,indent=5)

    print(f"collected data: {len(data)},saved into file: {fileName}")    

        

dataFetchurl = "https://hacker-news.firebaseio.com/v0/topstories.json"

# Fetch the data from the url, converting it into json and then storing 500 entries into storyIdsJson
storyIdsJson = (requests.get(dataFetchurl)).json()[:500]
# print(f"sotyIdsJson: {storyIdsJson}")

collectedData = fetchStories(storyIdsJson)
savetoJSON(collectedData)

