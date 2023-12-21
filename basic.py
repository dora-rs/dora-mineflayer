import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

from javascript import require, On
from dora import Node
import pyarrow as pa
from typing import Callable, Optional, Union
from dora import DoraStatus

mineflayer = require('mineflayer')
viewer = require('prismarine-viewer').mineflayer
pathfinder = require('mineflayer-pathfinder')

RANGE_GOAL = 1
BOT_USERNAME = 'python'

node = Node()

bot = mineflayer.createBot({
  #'host': '3000',
  'port': 55567, 
  'username': BOT_USERNAME
})

bot.loadPlugin(pathfinder.pathfinder)
print("Started mineflayer")

@On(bot, 'spawn')
def handle(*args):
  print("I spawned 👋")
  movements = pathfinder.Movements(bot)
  for i in range(100):
    dora_event = node.next()
    if dora_event["type"] == "INPUT":
      match dora_event["id"]:
        case "tick":
          viewer(bot, {'port': 3000, 'firstPerson': True})
          node.send_output('image', pa.array([]))
    @On(bot, 'chat')
    def handleMsg(this, sender, message, *args):
      
      node.send_output('chat', pa.array([message]))
      print("Got message", sender, message)
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
