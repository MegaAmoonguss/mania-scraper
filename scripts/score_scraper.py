import sqlite3
import json
import requests
import bs4

# get user data
res = requests.get("https://new.ppy.sh/u/5572803")
 
user = ""
for i in res.text:
    try:
        user += i
    except UnicodeEncodeError:
        pass
 
soup = bs4.BeautifulSoup(user, "html.parser")
tag = soup.find("script", {"id": "json-user", "type": "application/json"})
user_data = json.loads(str(tag)[47:-9].strip())

# get score data
username, title, version, rating, score, accuracy = (
    user_data["username"],
    user_data["allScoresBest"]["mania"][0]["beatmapset"]["title"],
    user_data["allScoresBest"]["mania"][0]["beatmap"]["version"],
    "%.2f" % (user_data["allScoresBest"]["mania"][0]["beatmap"]["difficulty_rating"]),
    user_data["allScoresBest"]["mania"][0]["score"],
    "%.2f" % (user_data["allScoresBest"]["mania"][0]["accuracy"] * 100)
    )

# load scores to database
conn = sqlite3.connect("mania_data.db")
c = conn.cursor()
 
try:
    c.execute("SELECT * FROM mania")
except sqlite3.OperationalError:
    c.execute("CREATE TABLE mania (username text, title text, version text, rating real, score real, accuracy real)")
 
c.execute(f"INSERT INTO mania VALUES ('{username}', '{title}', '{version}', {rating}, {score}, {accuracy})")
for row in c.execute("SELECT * FROM mania"):
    print(row)
     
conn.commit()
conn.close()
