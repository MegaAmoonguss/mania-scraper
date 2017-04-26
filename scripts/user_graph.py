import sys
import json
import matplotlib.pyplot as plt

username = input("Enter user: ")

try:
    with open(f"../users/{username}.json") as file:
        user_data = json.load(file)
except FileNotFoundError:
    print("User not found!")
    sys.exit(2)

songs = []

for i in range(100):
    try:
        current_song = [
            user_data["allScoresBest"]["mania"][i]["beatmapset"]["title"],
            user_data["allScoresBest"]["mania"][i]["beatmap"]["version"],
            user_data["allScoresBest"]["mania"][i]["mods"],
            user_data["allScoresBest"]["mania"][i]["beatmap"]["difficulty_rating"],
            user_data["allScoresBest"]["mania"][i]["score"]
        ]
    except IndexError:
        break

    if "HT" in current_song[2]:
        current_song[3] *= 0.795
    elif "DT" in current_song[2] or "NC" in current_song[2]:
        current_song[3] *= 1.38

    songs.append(current_song)

xvals = []
yvals = []
for song in songs:
    xvals.append(song[3])
    yvals.append(song[4])

plt.plot(xvals, yvals, 'o')
plt.axis([4.4, 7.1, 500000, 1000000])
plt.show()
