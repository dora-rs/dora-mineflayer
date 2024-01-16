from javascript import require, On
from dora import Node
import pyarrow as pa
import time
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
viewer = require('prismarine-viewer').mineflayer

RANGE_GOAL = 1
BOT_USERNAME = 'bot'
PORT = 62409
node = Node()

bot = mineflayer.createBot({
    'host': '127.0.0.1',
    'port': PORT, 
    'username': BOT_USERNAME
})

bot.loadPlugin(pathfinder.pathfinder)

@On(bot, 'spawn')
def handle(*args):
    is_item_activated = False
    activation_time = time.time()
    viewer(bot, {'port': 3000, 'firstPerson': True})
    node.send_output('stream', pa.array([]))
    movements = pathfinder.Movements(bot)
    bow = bot.inventory.findInventoryItem('bow')
    arrow = bot.inventory.findInventoryItem('arrow')
    if not bow:
        bot.chat("/give @s minecraft:bow")
        bow = bot.inventory.findInventoryItem('bow')
    bot.equip(bow, 'hand')
    if not arrow:
        bot.chat("/give @s minecraft:arrow 64")
    
    for event in node:
        if event["type"] == "INPUT":
            match event["id"]:
                case "coordinates":
                    [x, y, z] = event["value"].to_pylist()
                    bot.pathfinder.setMovements(movements)
                    bot.pathfinder.setGoal(pathfinder.goals.GoalNear(x, y, z, RANGE_GOAL))
                case "shoot":
                    if not is_item_activated:
                        is_item_activated = True
                        bot.activateItem()
                        activation_time = time.time()
                case "tick":
                    if is_item_activated and time.time() - activation_time > 1.5:
                        bot.deactivateItem()
                        is_item_activated = False
                case "aim":
                    [x, y] = event["value"].to_pylist()
                    x = bot.entity.yaw + x
                    bot.look(x, bot.entity.pitch, True)
@On(bot, "end")
def handle(*args):
    print("Bot ended!", args)

