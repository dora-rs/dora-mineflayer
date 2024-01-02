#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import time
import os
import cv2
import numpy as np
from dora import Node

CI = os.environ.get("CI")
HEIGHT = 683
WIDTH = 1366
node = Node()
frame = []
image_message = 0
bboxs = []
image_path = "../Images/screenshot.png"
for i in range(100):
    event = node.next()
    if event is not None:
        if event["type"] == "INPUT":
            if event["id"] == "image":
                image = cv2.imread(image_path)
                cv2.imshow("frame", image)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    exit()