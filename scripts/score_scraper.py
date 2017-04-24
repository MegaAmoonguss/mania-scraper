import json

song_list = [
    ["Speedcore 300", "Extra", []],
    ["croiX", "GRAVITY", []],
    ["over the top", "Extra", []],
    ["Blastix Riotz", "Jinjin s INFINITE", []],
    ["HAELEQUIN", "INF", []],
    ["Bangin  Burst", "EXHAUST Lv.16", []],
    ["Verse IV", "INFINITE", []],
    ["Tokyo Teddy Bear", "SHD", []],
    ["Galaxy Collapse", "Cataclysmic Hypernova", []],
    ["M.A.M.A.", "SHD", []],
    ["Kakuzetsu Thanatos", "Isolation", []],
    ["G1ll35 d3 R415", "L45T C4LL", []],
    ["LegenD.", "KK s GRAVITY", []],
    ["C18H27NO3(extend)", "4K Capsaicin", []],
    ["BLACK or WHITE?", "DECADE vs. Usagi s INFINITE Lv.16", []],
    ["Lachryma<Re:Queen M>", "GRAVITY", []],
    ["Hesperides", "Master", []],
    ["Bokutachi no Tabi to Epilogue.[Long ver.]", "Final Voyage", []],
    ["G1ll35 d3 R415", "Shana s Extra", []],
    ["Space Time (Amane Hardcore Remix)", "Spy s 4K Extra", []],
]

data = {}
for song in song_list:
    data[f"{song[0]} [{song[1]}]"] = []

with open("../data/working_users.txt") as file:
    working_users = eval(file.read())

for user in working_users:
    with open(f"../users/{user}.json") as file:
        user_data = json.load(file)

    for i in range(100):
        try:
            current_song = [
                user_data["allScoresBest"]["mania"][i]["beatmapset"]["title"].replace("'", " ").replace('"', " "),
                user_data["allScoresBest"]["mania"][i]["beatmap"]["version"].replace("'", " ").replace('"', " "),
                user_data["allScoresBest"]["mania"][i]["mods"]
            ]
        except IndexError:
            break

        if current_song in song_list:
            data[f"{current_song[0]} [{current_song[1]}]"].append(user_data["allScoresBest"]["mania"][i]["score"])

with open("../data/scores.json", 'w') as file:
    json.dump(data, file)
