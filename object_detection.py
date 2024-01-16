#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from ultralytics import YOLO

from dora import Node
import pyarrow as pa

CAMERA_WIDTH = 960
CAMERA_HEIGHT = 454

model = YOLO("yolov8n.pt")

node = Node()

for event in node:
    event_type = event["type"]
    if event_type == "INPUT":
        event_id = event["id"]
        if event_id == "image":
            print("[object detection] received image input")
            frame = (
                    event["value"]
                    .to_numpy()
                    .reshape((CAMERA_HEIGHT, CAMERA_WIDTH, 3))
                )
            results = model(frame)
            boxes = np.array(results[0].boxes.xyxy.cpu())
            conf = np.array(results[0].boxes.conf.cpu())
            label = np.array(results[0].boxes.cls.cpu())
            arrays = np.concatenate((boxes, conf[:, None], label[:, None]), axis=1)
            node.send_output("bbox", pa.array(arrays.ravel()), event["metadata"])
        else:
            print("[object detection] ignoring unexpected input:", event_id)
    elif event_type == "STOP":
        print("[object detection] received stop")
    elif event_type == "ERROR":
        print("[object detection] error: ", event["error"])
    else:
        print("[object detection] received unexpected event:", event_type)