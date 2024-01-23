from dora import Node
import pyarrow as pa
from selenium import webdriver
import numpy as np
import time
import cv2

node = Node()
driver = None
for event in node:
    if event["type"] == "INPUT":
        match event["id"]:
            case "stream":
                options = webdriver.FirefoxOptions()
                options.add_argument("--headless")
                driver = webdriver.Firefox(options=options)
                driver.set_window_size(960 , 540) 
                driver.get("localhost:3000")
            case "tick":
                if driver is not None:
                    screenshot = driver.get_screenshot_as_png()
                    nparr = np.frombuffer(screenshot, np.uint8)
                    cv2_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    cv2.resize(cv2_image, (960, 540))
                    
                    node.send_output(
                        "image",
                        pa.array(cv2_image.ravel())
                    )
