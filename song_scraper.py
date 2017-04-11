import sqlite3
import json
import requests
import bs4

# initiate database connection
conn = sqlite3.connect("songs.db")
c = conn.cursor()

try:
    c.execute("DROP TABLE songs")
except sqlite3.OperationalError:
    pass
c.execute("CREATE TABLE songs (title text, version text, count real)")

# TODO: Get data for top 3000 ranks
rank = 1
for i in range(1, 61):
    res = requests.get(f"https://osu.ppy.sh/p/pp/?m=3&s=3&o=1&f=&page={i}")
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    table = soup.find_all("tr")

    for r in range(1, 51):
        print(f"{rank}. " + table[r].find("a")["href"])
        rank += 1
    
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

# get song count info
for i in range(100):
    title, version = (
        user_data["allScoresBest"]["mania"][i]["beatmapset"]["title"].replace("'", "").replace('"', ''),
        user_data["allScoresBest"]["mania"][i]["beatmap"]["version"].replace("'", "").replace('"', '')
        )
    
    # add to database
    entry = c.execute(f"SELECT * FROM songs WHERE title='{title}' AND version='{version}'")
    if not entry.fetchall():
        c.execute(f"INSERT INTO songs VALUES ('{title}', '{version}', 1)")
    else:
        c.execute(f"UPDATE songs SET count = count + 1 WHERE title='{title}' AND version='{version}'")
    
for row in c.execute("SELECT * FROM songs"):
    print(row)
    
conn.commit()
conn.close()
