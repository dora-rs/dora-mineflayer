from javascript import require, On
from dora import Node
import pyarrow as pa
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
viewer = require('prismarine-viewer').mineflayer

RANGE_GOAL = 1
BOT_USERNAME = 'bot'
PORT = 54176
node = Node()

bot = mineflayer.createBot({
    'host': '127.0.0.1',
    'port': PORT, 
    'username': BOT_USERNAME
})

bot.loadPlugin(pathfinder.pathfinder)

@On(bot, 'spawn')
def handle(*args):
    movements = pathfinder.Movements(bot)
    viewer(bot, {'port': 3000, 'firstPerson': True})
    node.send_output('stream', pa.array([]))

    @On(bot, 'chat')
    def handleMsg(this, sender, message, *args):
        if sender and (sender != BOT_USERNAME):
            bot.chat('Hi, you said ' + message)
            if 'come' in message:
                player = bot.players[sender]
                print("Target", player)
                target = player.entity
                if not target:
                    bot.chat("I don't see you !")
                    return

            pos = target.position
            bot.pathfinder.setMovements(movements)
            bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))

@On(bot, "end")
def handle(*args):
    print("Bot ended!", args)
