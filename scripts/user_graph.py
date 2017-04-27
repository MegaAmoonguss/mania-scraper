import sys
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import scipy.stats

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

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
x_bestfit = np.linspace(0, 11, num=50)
y_bestfit = np.linspace(intercept, slope * 11 + intercept, num=50)

plt.rc("grid", linestyle="--")
plt.scatter(x, y)
plt.plot(x_bestfit, y_bestfit, 'r')
plt.axis([4.4, 7.1, 500, 1000])

plt.title(f"Profile Data for {username}")
plt.xlabel("Difficulty Rating (stars)")
plt.ylabel("Score (1000s)")

plt.grid(True)
red_patch = mpatches.Patch(color='r', label=f"Best fit line\nr^2 = {r_value**2}")
plt.legend(handles=[red_patch])

plt.show()