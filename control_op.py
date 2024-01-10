from dora import Node
import pyarrow as pa

node = Node()

for i in range(1000):
    event = node.next()
    if event is not None:
        if event["type"] == "INPUT":
            match event["id"]:
                case "move":
                    
                    node.send_output("image", pa.array([])) 
                case "tick":
                    pass