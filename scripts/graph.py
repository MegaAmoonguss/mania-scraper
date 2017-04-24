import json
import matplotlib.pyplot as plt

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

with open("../data/scores.json") as file:
    data = json.load(file)

with open("../users/MegaAmoonguss.json") as file:
    user_data = json.load(file)

ratings = {}
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
        key = f"{current_song[0]} [{current_song[1]}]"
        ratings[key] = user_data["allScoresBest"]["mania"][i]["beatmap"]["difficulty_rating"]

graph_data = {}
for key in data:
    graph_data[key] = [ratings[key], sum(data[key]) / len(data[key])]

xvals = []
yvals = []
for key in graph_data:
    xvals.append(graph_data[key][0])
    yvals.append(graph_data[key][1])

print(graph_data)
plt.plot(xvals, yvals, 'o')
plt.axis([4.5, 7, 500000, 1000000])
plt.show()
