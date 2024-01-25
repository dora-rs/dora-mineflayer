from dora import DoraStatus
import keyboard
import pyarrow as pa
from typing import Callable, Optional, Union

class Operator:
    def __init__(self):
        self.key_pressed = False
        
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
        if dora_input["id"] == "tick":
            # Check if the 'm' key is currently pressed
            if keyboard.is_pressed('m'):
                # Key is pressed
                if not self.key_pressed:
                    print("Key 'm' pressed")
                    self.key_pressed = True
                    send_output("mic_on", pa.array([]))
            else:
                # Key is released
                if self.key_pressed:
                    self.key_pressed = False
        return DoraStatus.CONTINUE
