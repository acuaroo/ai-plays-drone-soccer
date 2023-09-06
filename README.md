# AI plays drone soccer

> _Goal: Train an AI to play [drone soccer](https://www.dronesoccer.us/), and play against other huamans/AI_

## What's drone soccer?

Essentially, on each team, there's a "striker". This striker must pilot their drone into the enemy teams goal, everybody on their team blocks the enemies striker, and everybody on the opposing team blocks them. More in-depth rules can be found [here](https://www.dronesoccer.us/intro), but for our purposes, this should be good enough!

## Stage 0: Prep

For the drone, I went for the [Tello](https://www.ryzerobotics.com/tello), due to it's easy [python API](https://djitellopy.readthedocs.io/en/latest/), small size, and being relatively cheap (allowing me to upscale to more drones).

## Stage 1: Training

First step is training, in this, we're going to teach a drone how to go through the hoop. To collect training data, I've set up a bluetooth server (`bluetooth-server.py`), where a video game controller connects to the PC, and the PC relays the commands to the drone. I have to use this relay approach as I need to record data, which their app doesn't allow you to do.

---

> _Project is still a WIP_
