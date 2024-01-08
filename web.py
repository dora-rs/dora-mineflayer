from dora import Node
import pyarrow as pa
from selenium import webdriver
import numpy as np
import time

node = Node()
driver = None
for i in range(1000):
    event = node.next()
    if event is not None:
        if event["type"] == "INPUT":
            match event["id"]:
                case "stream":
                    time.sleep(3)
                    options = webdriver.FirefoxOptions()
                    options.add_argument("--headless")
                    driver = webdriver.Firefox(options=options)
                    driver.set_window_size(960 , 540) 
                    driver.get("localhost:3000")
                case "tick":
                    if driver is not None:
                        driver.save_screenshot("../Images/screenshot.png")
                        """screenshot = driver.get_screenshot_as_png()
                        nparr = np.frombuffer(screenshot, np.uint8)
                        print(driver.get_window_size(), flush=True)"""
                        
                        #node.send_output("image", pa.array(nparr)) 
                        node.send_output("image", pa.array([])) 
                
                