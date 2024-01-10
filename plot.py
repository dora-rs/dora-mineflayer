#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from dora import Node
from utils import LABELS

CAMERA_WIDTH = 960
CAMERA_HEIGHT = 454

CI = os.environ.get("CI")
node = Node()
bounding_box_messages = 0
bboxs = []
for event in node:
    if event["type"] == "INPUT":
        if event["id"] == "image":
            cv2_image = (
                event["value"]
                .to_numpy()
                .reshape((CAMERA_HEIGHT, CAMERA_WIDTH, 3))
                .copy()  # copy the image because we want to modify it below
            )
        if event["id"] == "bbox":
            bboxs = event["value"].to_numpy()
            bboxs = np.reshape(bboxs, (-1, 6))

            bounding_box_messages += 1
            print("received " + str(bounding_box_messages) + " bounding boxes")
        
        for bbox in bboxs:
            [ 
                min_x,
                min_y,
                max_x,
                max_y,
                confidence,
                label,
            ] = bbox
            cv2.rectangle(
                cv2_image,
                (int(min_x), int(min_y)),
                (int(max_x), int(max_y)),
                (0, 255, 0),
                2,
            )
            cv2.putText(
                cv2_image,
                LABELS[int(label)],
                (int(max_x), int(max_y)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 255, 0),
                2,
                1,
            )
                
        cv2.imshow("frame", cv2_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            exit()
            