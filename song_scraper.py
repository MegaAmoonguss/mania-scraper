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
c.execute("CREATE TABLE songs (title text, version text, mods text, creator text, rating float, count integer)")

# get top users
top_users = []
for i in range(1, 2):
    res = requests.get(f"https://osu.ppy.sh/p/pp/?m=3&s=3&o=1&f=&page={i}")
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    table = soup.find_all("tr")

    for r in range(1, 4):
        top_users.append(table[r].find("a")["href"])

# iterate through the users
num = 1
for link in top_users:
    print(f"{num}. {link}")
    num += 1

    # get user data
    res = requests.get("https://new.ppy.sh" + link)

    user = ""
    for i in res.text:
        try:
            user += i
        except UnicodeEncodeError:
            pass

    soup = bs4.BeautifulSoup(user, "html.parser")
    tag = soup.find("script", {"id": "json-user", "type": "application/json"})
    user_data = json.loads(str(tag)[47:-9].strip())

    # save user data
    with open("users/" + user_data["username"] + ".json", "w") as file:
        json.dump(user_data, file)

    # get song count info
    for i in range(100):
        title, version, mods, creator, rating = (
            user_data["allScoresBest"]["mania"][i]["beatmapset"]["title"].replace("'", "").replace('"', ''),
            user_data["allScoresBest"]["mania"][i]["beatmap"]["version"].replace("'", "").replace('"', ''),
            user_data["allScoresBest"]["mania"][i]["mods"],
            user_data["allScoresBest"]["mania"][i]["beatmapset"]["creator"],
            user_data["allScoresBest"]["mania"][i]["beatmap"]["difficulty_rating"]
        )

        # add to database
        entry = c.execute(f"SELECT * FROM songs WHERE title='{title}' AND version='{version}'")
        if not entry.fetchall():
            c.execute(f"INSERT INTO songs "
                      f"VALUES ('{title}', '{version}', '{' '.join(mods)}', '{creator}', {rating}, 1)")
        else:
            c.execute(f"UPDATE songs SET count = count + 1 "
                      f"WHERE title='{title}' "
                      f"AND version='{version}' "
                      f"AND mods='{' '.join(mods)}' "
                      f"AND creator='{creator}'")

# print out the table
for row in c.execute("SELECT * FROM songs ORDER BY count DESC"):
    print(row)

conn.commit()
conn.close()
