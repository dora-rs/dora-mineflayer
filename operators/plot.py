#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import pyarrow as pa
from dora import DoraStatus
from typing import Callable, Optional, Union
from utils import LABELS
import math
CAMERA_WIDTH = 960
CAMERA_HEIGHT = 455

CI = os.environ.get("CI")


def calculate_center_movement(WIDTH, HEIGHT, boxes):
    image_center = np.array([WIDTH / 2, (HEIGHT + 60) / 2])
    min_distance = float('inf')
    closest_box = None

    for box in boxes:
        box_center = np.array([(box[0] + box[2]) / 2, (box[1] + box[3]) / 2])
        distance = np.linalg.norm(image_center - box_center)

        if distance < min_distance:
            min_distance = distance
            closest_box = box_center

    if closest_box is not None:
        movement = image_center - closest_box
    else:
        movement = np.array([0, 0])

    return movement

def calculate_turn_angles(width, height, fov, cow_offset):
    # Convert FOV to radians
    fov_rad = math.radians(fov)

    # Calculate the horizontal and vertical angles in radians
    horizontal_angle_rad = math.atan2(cow_offset[0], width / (2 * math.tan(fov_rad / 2)))
    vertical_angle_rad = math.atan2(cow_offset[1], height / (2 * math.tan(fov_rad / 2)))

    return horizontal_angle_rad, vertical_angle_rad

class Operator:
    """
    Plot image and bounding box
    """

    def __init__(self):
        self.image = []
        self.bboxs = []
        self.bounding_box_messages = 0
        self.image_messages = 0
        self.text_whisper = ""
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
        if dora_input["id"] == "image":
            frame = (
                dora_input["value"]
                .to_numpy()
                .reshape((CAMERA_HEIGHT, CAMERA_WIDTH, 3))
                .copy()  # copy the image because we want to modify it below
            )
            self.image = frame

            self.image_messages += 1
            print("received " + str(self.image_messages) + " images")
            
        elif dora_input["id"] == "bbox" and len(self.image) != 0:
            bboxs = dora_input["value"].to_numpy()
            self.bboxs = np.reshape(bboxs, (-1, 6))

            self.bounding_box_messages += 1
            print("received " + str(self.bounding_box_messages) + " bounding boxes")
        elif dora_input["id"] == "text" and len(self.image) != 0:
            self.text_whisper = dora_input["value"][0].as_py()
        persons = []
        for bbox in self.bboxs:
            [ 
                min_x,
                min_y,
                max_x,
                max_y,
                confidence,
                label,
            ] = bbox
            
            if label == 0:
                persons.append([min_x, min_y, max_x, max_y])
                    
            cv2.rectangle(
                self.image,
                (int(min_x), int(min_y)),
                (int(max_x), int(max_y)),
                (0, 255, 0),
                2,
            )
            cv2.putText( 
                self.image,
                LABELS[int(label)],
                (int(max_x), int(max_y)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 255, 0),
                2,
                1,
            )

        cv2.putText(
            self.image, self.text_whisper, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 250, 250), 2, 1
        )   
            
            
        if len(persons) > 0:
            move = calculate_center_movement(CAMERA_WIDTH, CAMERA_HEIGHT, persons)
            turn = calculate_turn_angles(CAMERA_WIDTH, CAMERA_HEIGHT, 70, move)
            send_output("aim", pa.array(turn))
            persons = []
        
        if CI != "true":
            cv2.imshow("frame", self.image)
            if cv2.waitKey(1) == ord("q"):
                send_output("mic", pa.array([]))
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                return DoraStatus.STOP
        return DoraStatus.CONTINUE

    def __del__(self):
        cv2.destroyAllWindows()
