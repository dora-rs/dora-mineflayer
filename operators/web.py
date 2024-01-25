from dora import DoraStatus
import pyarrow as pa
from typing import Callable, Optional, Union
from selenium import webdriver
import numpy as np
import time
import cv2

class Operator:
    
    def __init__(self):
        self.driver = None
    
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
        if dora_input["id"] == "stream":
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Firefox(options=options)
            self.driver.set_window_size(960 , 540) 
            self.driver.get("localhost:3000")
        elif dora_input["id"] == "tick":
            if self.driver is not None:
                screenshot = self.driver.get_screenshot_as_png()
                nparr = np.frombuffer(screenshot, np.uint8)
                cv2_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.resize(cv2_image, (960, 540))
                
                send_output(
                    "image",
                    pa.array(cv2_image.ravel())
                )
        return DoraStatus.CONTINUE
