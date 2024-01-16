#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import pyarrow as pa
from dora import Node
from utils import LABELS
import math
CAMERA_WIDTH = 960
CAMERA_HEIGHT = 454

CI = os.environ.get("CI")
node = Node()
bounding_box_messages = 0
bboxs = []


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
        
        persons = []
        for bbox in bboxs:
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
        if len(persons) > 0:
            move = calculate_center_movement(CAMERA_WIDTH, CAMERA_HEIGHT, persons)
            turn = calculate_turn_angles(CAMERA_WIDTH, CAMERA_HEIGHT, 70, move)
            #print("move :", move, flush=True)
            #print("turn :", turn, flush=True)
            node.send_output("turn", pa.array(turn))
            persons = []
        
        cv2.imshow("frame", cv2_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            exit()

