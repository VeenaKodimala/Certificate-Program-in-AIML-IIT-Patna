import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
import sqlite3

DB="TMDBDataBase"
BaseUrl="https://api.themoviedb.org/3"

def createDBTbls():
   
   conn = sqlite3.connect(DB)
   cursor = conn.cursor()

   cursor.executescript("""
                      PRAGMA journal_mode=WAL;
                      CREATE TABLE IF NOT EXISTS movies (
                      movie_id INTEGER PRIMARY KEY,
                      title TEXT    NOT NULL,
                      original_title TEXT,
                      release_date TEXT,
                      release_year INTEGER,
                      release_month INTEGER,
                      runtime           INTEGER,
                      budget            REAL,
                      revenue           REAL,
                      vote_average      REAL,
                      vote_count        INTEGER,
                      popularity        REAL,
                      original_language TEXT,
                      overview          TEXT,
                      tagline           TEXT,
                      is_franchise      INTEGER DEFAULT 0,
                      collection_name   TEXT,
                      fetched_at        TEXT
                      );
                      CREATE TABLE IF NOT EXISTS genres (
                      genre_id   INTEGER PRIMARY KEY,
                      genre_name TEXT NOT NULL
                      );
                      CREATE TABLE IF NOT EXISTS movie_genres (
                      movie_id   INTEGER,
                      genre_id   INTEGER,
                      genre_name TEXT,
                      PRIMARY KEY (movie_id, genre_id),
                      FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
                      FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
                      );
                      CREATE TABLE IF NOT EXISTS cast (
                      id    INTEGER PRIMARY KEY AUTOINCREMENT,
                      movie_id     INTEGER,
                      actor_name   TEXT,
                      character    TEXT,
                      billing_order INTEGER,
                      person_id    INTEGER,
                      FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
                      );
                      CREATE TABLE IF NOT EXISTS directors (
                      id    INTEGER PRIMARY KEY AUTOINCREMENT,
                      movie_id     INTEGER UNIQUE,
                      director_name TEXT,
                      person_id    INTEGER,
                      FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
                      );""")
   conn.commit()
   print("Database created:", DB)
   print("Tables created:")
   query="SELECT name FROM sqlite_master WHERE type='table'"
   cursor.execute(query)
   tables = cursor.fetchall()
   conn.close()

   for table in tables:
      print(f"Table name:{table}")

#Function to fetch the genere from TMDB API and inserting into genre table.
def insertGenres(apiKey):
   try:
      params = {"api_key":apiKey}
      print(f"{BaseUrl}/genre/movie/list")
      resp = requests.get(f"{BaseUrl}/genre/movie/list"
                          ,params=params)
      genres=resp.json()['genres']
      #print(f"type of genres: {genres}")
      
      conn = sqlite3.connect(DB)
      cursor = conn.cursor()

      cursor.executemany("INSERT INTO genres(genre_id,genre_name)" \
      "VALUES (?,?)", [(g['id'],g['name']) for g in genres])

      print(f"Checking if rows inserted: {cursor.execute("SELECT count(*) FROM genres").fetchone()}")
      conn.commit()
      conn.close()
   except Exception as e:
      print(f"Exception occured in insertGenres:: {e}")   

print("-----STEP-1: Load API KEY-----")
load_dotenv()
apiKey = os.getenv("Tmdb_Api_Key")
print("API Key loaded successfully")
print("-----CREATEING TABLES IN DATABASE-----")
createDBTbls()

insertGenres(apiKey=apiKey)


