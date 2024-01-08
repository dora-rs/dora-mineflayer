#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from dora import Node

CI = os.environ.get("CI")
node = Node()
image_path = "../Images/screenshot.png"
for i in range(1000):
    event = node.next()
    if event is not None:
        if event["type"] == "INPUT":
            if event["id"] == "image":
                """nparr = np.array(event["value"])
                nparr_reshaped = nparr.reshape((540, -1, 3))
                cv2_image = cv2.cvtColor(nparr, cv2.COLOR_BGR2RGB)"""
                cv2_image = cv2.imread(image_path)
                cv2.imshow("frame", cv2_image)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    exit()