import os
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
        tag = table[r].find("a")
        top_users.append((tag["href"], tag.contents[0]))

# iterate through the users
num = 1
for user_id in top_users:
    print(f"{num}. {user_id[1]}")
    num += 1

    # get user data
    if os.path.isfile("users/" + user_id[1] + ".json"):
        # get saved data if it exists
        with open("users/" + user_id[1] + ".json") as file:
            user_data = json.load(file)
            print(user_data)
    else:
        res = requests.get("https://new.ppy.sh" + user_id[0])

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
            user_data["allScoresBest"]["mania"][i]["beatmapset"]["title"].strip("\"'"),
            user_data["allScoresBest"]["mania"][i]["beatmap"]["version"].strip("\"'"),
            user_data["allScoresBest"]["mania"][i]["mods"],
            user_data["allScoresBest"]["mania"][i]["beatmapset"]["creator"],
            user_data["allScoresBest"]["mania"][i]["beatmap"]["difficulty_rating"]
        )
        dt = ""
        if "DT" in mods or "NC" in mods:
            dt = "dt"

        # add to database
        entry = c.execute(f"SELECT * FROM songs "
                          f"WHERE title='{title}' "
                          f"AND version='{version}' "
                          f"AND mods='{dt}' "
                          f"AND creator='{creator}'")
        if not entry.fetchall():
            c.execute(f"INSERT INTO songs "
                      f"VALUES ('{title}', '{version}', '{dt}', '{creator}', {rating}, 1)")
        else:
            c.execute(f"UPDATE songs SET count = count + 1 "
                      f"WHERE title='{title}' "
                      f"AND version='{version}' "
                      f"AND mods='{dt}' "
                      f"AND creator='{creator}'")

# print out the table
for row in c.execute("SELECT * FROM songs ORDER BY count DESC"):
    print(row)

conn.commit()
conn.close()
