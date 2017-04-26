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
        current_song[4] *= 2
    elif "DT" in current_song[2] or "NC" in current_song[2]:
        current_song[3] *= 1.38

    songs.append(current_song)

x = []
y = []
for song in songs:
    x.append(song[3])
    y.append(song[4] / 1000)

plt.rc("grid", linestyle="--")
plt.scatter(x, y)
plt.axis([4.4, 7.1, 500, 1000])

plt.title(f"Profile Data for {username}")
plt.xlabel("Difficulty Rating (stars)")
plt.ylabel("Score (1000s)")

plt.grid(True)
plt.show()
