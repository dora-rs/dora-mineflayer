from javascript import require, On
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
from time import sleep
RANGE_GOAL = 1
BOT_USERNAME = 'python'

bot = mineflayer.createBot({
    'host': '127.0.0.1',
    'port':  53624,
    'username': BOT_USERNAME
})

bot.loadPlugin(pathfinder.pathfinder)
print("Started mineflayer")

@On(bot, 'spawn')
def handle(*args):
    print("I spawned 👋")
    movements = pathfinder.Movements(bot)

    @On(bot, 'chat')
    def handleMsg(this, sender, message, *args):
        print("Got message", sender, message)
        if sender and (sender != BOT_USERNAME):
            bot.chat('Hi, you said ' + message)
            if 'come' in message:
                bot.activateItem()
                sleep(1)
                bot.deactivateItem()

@On(bot, "end")
def handle(*args):
    print("Bot ended!", args)
