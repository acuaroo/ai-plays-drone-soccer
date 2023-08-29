import os

directory = "data/"
states = {}

def index_images(dir):
    for file_name in os.listdir(dir):
        file = os.path.join(directory, file_name)

        if not file:
            continue

        state = file_name.split("_")[2]

        if not states.get(state):
            states[state] = 1
        else:
            states[state] += 1


for directory_name in os.listdir("data/"):
    dir = os.path.join(directory, directory_name)

    if os.path.isdir(dir):
        index_images(dir)

print(states)