import os
import sqlite3
import json
import requests
import bs4

# initiate database connection
conn = sqlite3.connect("./data/songs.db")
c = conn.cursor()

try:
    c.execute("DROP TABLE songs")
except sqlite3.OperationalError:
    pass
c.execute("CREATE TABLE songs (title text, version text, mods text, creator text, rating float, count integer)")

# get top users
# NOTE: will not work if file does not exist
top_users = []
with open("./data/top3000.txt") as file:
    # if list needs to be generated
    # for i in range(1, 61):
    #     res = requests.get(f"https://osu.ppy.sh/p/pp/?m=3&s=3&o=1&f=&page={i}")
    #     soup = bs4.BeautifulSoup(res.text, "html.parser")
    #     table = soup.find_all("tr")

    #     for r in range(1, 51):
    #         tag = table[r].find("a")
    #         top_users.append((tag["href"], tag.contents[0]))
    #         file.write(tag["href"] + "," + tag.contents[0] + "\n")

    # parse existing file
    for line in file.readlines():
        link, name = line.rstrip().split(",")
        top_users.append((link, name))

try:
    # iterate through the users
    index = 0
    for user_id in top_users:
        print(f"{index}. {user_id[1]}")
        index += 1

        # get user data
        if os.path.isfile("./users/" + user_id[1] + ".json"):
            # get saved data if it exists
            with open("./users/" + user_id[1] + ".json") as file:
                user_data = json.load(file)

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
            try:
                user_data = json.loads(str(tag)[47:-9].strip())
            except json.JSONDecodeError:
                print("JSONDecodeError encountered! Skipping")
                continue

            # save user data
            with open("./users/" + user_data["username"] + ".json", "w") as file:
                json.dump(user_data, file)

        # get song count info
        for i in range(100):
            try:
                title, version, mods, creator, rating = (
                    user_data["allScoresBest"]["mania"][i]["beatmapset"]["title"].replace("'", " ").replace('"', " "),
                    user_data["allScoresBest"]["mania"][i]["beatmap"]["version"].replace("'", " ").replace('"', " "),
                    user_data["allScoresBest"]["mania"][i]["mods"],
                    user_data["allScoresBest"]["mania"][i]["beatmapset"]["creator"].replace("'", " ").replace('"', " "),
                    user_data["allScoresBest"]["mania"][i]["beatmap"]["difficulty_rating"]
                )
            except IndexError:
                break

            if "HD" in mods:
                del mods[mods.index("HD")]
            if "FL" in mods:
                del mods[mods.index("FL")]
            if "NC" in mods:
                mods[mods.index("NC")] = "DT"
            if "SD" in mods:
                del mods[mods.index("SD")]
            if "PF" in mods:
                del mods[mods.index("PF")]
            for k in range(1, 10):
                if "%dK" % k in mods:
                    del mods[mods.index("%dK" % k)]

            # add to database
            entry = c.execute(f"SELECT * FROM songs "
                              f"WHERE title='{title}' "
                              f"AND version='{version}' "
                              f"AND mods='{' '.join(mods)}' "
                              f"AND creator='{creator}'")
            if not entry.fetchall():
                c.execute(f"INSERT INTO songs "
                          f"VALUES ('{title}', '{version}', '{' '.join(mods)}', '{creator}', {rating}, 1)")
            else:
                c.execute(f"UPDATE songs SET count = count + 1 "
                          f"WHERE title='{title}' "
                          f"AND version='{version}' "
                          f"AND mods='{' '.join(mods)}' "
                          f"AND creator='{creator}'")

        # delete line in top3000.txt
        # with open("./data/top3000.txt", "w") as file:
        #     csv = [",".join(line) for line in top_users[index + 1:]]
        #     file.write("\n".join(csv))
except KeyboardInterrupt:
    # NOTE: while this will technically work even if you interrupt, some data will be duplicated, not recommended
    pass

# print out the table
# for row in c.execute("SELECT * FROM songs ORDER BY count DESC"):
#     print(row)
print("Done!")

conn.commit()
conn.close()
