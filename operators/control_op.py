from dora import DoraStatus

from typing import Callable, Optional, Union
import pyarrow as pa


GOAL_OBJECTIVE = [250, 3, -100]


class Operator:
    
    def __init__(self):
        pass
    
    def on_event(
        self,
        dora_event: dict,
        send_output: Callable[[str, Union[bytes, pa.Array], Optional[dict]], None],
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            return self.on_input(dora_event, send_output)
        return DoraStatus.CONTINUE

    def on_input(
        self,
        dora_input: dict,
        send_output: Callable[[str, Union[bytes, pa.Array], Optional[dict]], None],
    ) -> DoraStatus:
        match dora_input["id"]:
            case "text":
                text_input = dora_input["value"].to_pylist()[0] # Convert input text to lowercase
                if "dig" in text_input:
                    send_output("dig", pa.array([]))
                elif "drink" in text_input:
                    send_output("drink", pa.array([]))
                elif "move" in text_input:
                    send_output("move", pa.array(GOAL_OBJECTIVE))
                
            case "aim":
                send_output("shoot", pa.array([]))
        
        return DoraStatus.CONTINUE
