import os
import json

song_list = [
    ["Speedcore 300", "Extra"],
    ["croiX", "GRAVITY"],
    ["over the top", "Extra"],
    ["Blastix Riotz", "Jinjin s INFINITE"],
    ["HAELEQUIN", "INF"],
    ["Bangin  Burst", "EXHAUST Lv.16"],
    ["Verse IV", "INFINITE"],
    ["Tokyo Teddy Bear", "SHD"],
    ["Galaxy Collapse", "Cataclysmic Hypernova"],
    ["M.A.M.A.", "SHD"],
    ["Kakuzetsu Thanatos", "Isolation"],
    ["G1ll35 d3 R415", "L45T C4LL"],
    ["LegenD.", "KK s GRAVITY"],
    ["C18H27NO3(extend)", "4K Capsaicin"],
    ["BLACK or WHITE?", "DECADE vs. Usagi s INFINITE Lv.16"],
    ["Lachryma<Re:Queen M>", "GRAVITY"],
    ["Hesperides", "Master"],
    ["Bokutachi no Tabi to Epilogue.[Long ver.]", "Final Voyage"],
    ["G1ll35 d3 R415", "Shana s Extra"],
    ["Space Time (Amane Hardcore Remix)", "Spy s 4K Extra"],
]

working_users = []
for file in os.listdir("../users/"):
    with open(f"../users/{file}") as user:
        user_data = json.load(user)

    songs = []
    for i in range(100):
        try:
            current_song = [
                user_data["allScoresBest"]["mania"][i]["beatmapset"]["title"].replace("'", " ").replace('"', " "),
                user_data["allScoresBest"]["mania"][i]["beatmap"]["version"].replace("'", " ").replace('"', " "),
            ]
        except IndexError:
            break
        songs.append(current_song)

    user_works = True
    for song in song_list:
        if song not in songs:
            print(song)
            user_works = False
            break

    if user_works:
        working_users.append(file)

print(working_users)
with open("../data/working_users.txt", 'w') as file:
    file.write(str(working_users))
