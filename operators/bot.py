from javascript import require, On
from dora import Node
import pyarrow as pa
import time
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
viewer = require('prismarine-viewer').mineflayer
Vec3 = require('vec3')

RANGE_GOAL = 1
BOT_USERNAME = 'bot'
PORT = 57463
node = Node()

bot = mineflayer.createBot({
    'port': PORT,
    'username': BOT_USERNAME,
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

    if not bow:
        bot.chat("/give @s minecraft:bow")
        bow2 = bot.inventory.findInventoryItem('bow')
        bot.equip(bow2, 'hand')
        
    else:
        bot.equip(bow, 'hand')
    arrow = bot.inventory.findInventoryItem('arrow')
    if not arrow:
        bot.chat("/give @s minecraft:arrow 64")

    for event in node:
        if event["type"] == "INPUT":
            match event["id"]:
                case "move":
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
                case "drink":
                    potion = bot.inventory.findInventoryItem('potion')
                    if not potion:
                        bot.chat("/give @s minecraft:potion{Potion:\"minecraft:long_strength\"}")
                        potion = bot.inventory.findInventoryItem('potion')
                    if potion:
                        bot.equip(potion, 'hand')
                        bot.consume()
                        bot.equip(bow, 'hand')
                case "dig":
                    x, y, z = bot.entity.position
                    print(1, flush=True)
                    targetBlock = bot.blockAt(Vec3(x, y - 1, z))
                    if (bot.canDigBlock(targetBlock)) :
                        bot.dig(targetBlock)
