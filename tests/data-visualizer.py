import os
import matplotlib.pyplot as plt

directory = "data/"
states = {}

total_num = 0

def index_images(session_directory):
    global total_num
    print(session_directory)

    for file_name in os.listdir(session_directory):
        file = os.path.join(directory, file_name)

        if not file:
            continue

        # take the name 0_20-21-02_0_0_1_0_1.png and remove the id part (0_20-21-02)
        under_split = file_name.split("_")
        state_start = under_split[2:6]
        state_end = under_split[6].split(".")[0]

        state = "_".join(state_start) + "_" + state_end
        total_num += 1

        if not states.get(state):
            states[state] = 1
        else:
            states[state] += 1


for directory_name in os.listdir("data/"):
    session = os.path.join(directory, directory_name)

    if os.path.isdir(session):
        index_images(session)

sorted_states = sorted(states.items(), key=lambda x: x[1], reverse=True)
sorted_len = len(sorted_states)

name = "states & their frequencies, " + str(total_num) + " points"

plt.bar(range(sorted_len), [val[1] for val in sorted_states], align="center")
plt.xticks(range(sorted_len), [val[0] for val in sorted_states])
plt.xticks(rotation=45, ha="right")
plt.title(name)
plt.show()