# dora running on mineflayer!

## Installation

`pip install -r requirements.txt`
[PyTorch](https://pytorch.org/get-started/locally/) need to be installed beforehand

## Getting Started
After you install official Minecraft, you should have a Minecraft official launcher, open it, and follow the instructions here:
1. Select the version you want to play and start the game. This project is tested on 1.16.1.
2. Select `Singleplayer` and create a new world.
3. Set Game Mode to `Creative` and Difficulty to `Peaceful`.
4. After the world is created, press `Esc` and select `Open to LAN`.
5. Select `Allow cheats: ON` and press `Start LAN World`.
6. You will see a port number in the chat log, that is your `mc-port`, use this number to instantiate Voyager later.

### Start the dataflow

```bash
dora up
dora start graphs/dataflow.yml --attach --hot-reload
```
