from dora import Node
import pyarrow as pa

node = Node()
isshooting = False

for event in node:
    if event["type"] == "INPUT":
        match event["id"]:
            case "move":
                print("move",flush=True)
                [x, y, z] = event["value"].to_pylist()
                x += 5
                node.send_output("coordinates", pa.array([x, y, z])) 
            case "bot":
                print("bot",flush=True)
            case "aim":
                node.send_output("shoot", pa.array([]))
