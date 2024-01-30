import pynput
import pyarrow as pa

from dora import Node
from time import sleep

node = Node()

def on_key_release(key):
    try:
        if key.char == 'm':
            print("Key 'm' pressed up")
            node.send_output("mic_on", pa.array([]))
            
    except AttributeError:
        pass

pynput.keyboard.Listener(on_release=on_key_release).run()