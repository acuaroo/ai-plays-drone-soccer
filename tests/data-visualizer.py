import os
import matplotlib.pyplot as plt

directory = "data/"
states = {}


def index_images(session_directory):
    for file_name in os.listdir(session_directory):
        file = os.path.join(directory, file_name)

        if not file:
            continue

        state = file_name.split("_")[2]

        if not states.get(state):
            states[state] = 1
        else:
            states[state] += 1


for directory_name in os.listdir("data/"):
    session = os.path.join(directory, directory_name)

    if os.path.isdir(session):
        index_images(session)

plt.bar(*zip(*states.items()))
plt.title("states vs state frequency")
plt.show()
