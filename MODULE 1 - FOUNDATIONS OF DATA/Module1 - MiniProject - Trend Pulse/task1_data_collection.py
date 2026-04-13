import requests
from datetime import datetime

CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def fetchCategory(title):
    for key,value in CATEGORIES.items():
        for word in value:
            if(word in title):
                return key
    return None   

        
def fetchStories(storyIds):
    headers = {"User-Agent": "TrendPulse/1.0"}
    collected=[]
    category_count={cat:0 for cat in CATEGORIES}
    for storyID in storyIds:
        storyFetchurl=f"https://hacker-news.firebaseio.com/v0/item/{storyID}.json"
        storyJSON = requests.get(storyFetchurl,headers=headers).json()
        if not storyJSON or "title" not in storyJSON:
            continue
        title=storyJSON.get("title")
        print(f"storyJSON title: {title}")
        category=fetchCategory(title=title)
        print(f"category: {category}")
        if category and category_count[category] < 25:
            story={"post_id":storyJSON.get("id"),
                   "title":title,
                   "category":category,
                   "score":storyJSON.get("score"),
                   "num_comments":storyJSON.get("descendants"),
                   "author":storyJSON.get("by"),
                   "collected_at":datetime.now()
                    }
            #print(f"story: {story}")
            collected.append(story)
            category_count[category]+=1

            #Checking if all the values in category_count dict is 



dataFetchurl="https://hacker-news.firebaseio.com/v0/topstories.json"

#Fetch the data from the url, converting it into json and then storing 500 entries into storyIdsJson
storyIdsJson = (requests.get(dataFetchurl)).json()[:10]
#print(f"sotyIdsJson: {storyIdsJson}")

fetchStories(storyIdsJson)




