#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Callable, Optional, Union
import cv2
import numpy as np
from ultralytics import YOLO
from dora import DoraStatus
import pyarrow as pa

CAMERA_WIDTH = 960
CAMERA_HEIGHT = 454


class Operator:
    
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def on_input(
        self,
        dora_event: dict,
        send_output: Callable[[str, Union[bytes, pa.Array], Optional[dict]], None],
    ) -> DoraStatus:
        match dora_event["type"]:
            case "INPUT":
                event_id = dora_event["id"]
                if event_id == "image":
                    return self.on_event(dora_event, send_output)
            case "STOP":
                print("[object detection] received stop")
                return DoraStatus.STOP
            case "ERROR":
                print("[object detection] error: ", dora_event["error"])
                return DoraStatus.STOP
            case _:
                print("[object detection] received unexpected event:", dora_event["type"])
        return DoraStatus.CONTINUE
        
    def on_event(
        self,
        dora_input: dict,
        send_output: Callable[[str, Union[bytes, pa.array], Optional[dict]], None],
    ) -> DoraStatus:
        frame = (
                dora_input["value"]
                .to_numpy()
                .reshape((CAMERA_HEIGHT, CAMERA_WIDTH, 3))
            )
        results = self.model(frame)
        boxes = np.array(results[0].boxes.xyxy.cpu())
        conf = np.array(results[0].boxes.conf.cpu())
        label = np.array(results[0].boxes.cls.cpu())
        arrays = np.concatenate((boxes, conf[:, None], label[:, None]), axis=1)
        send_output("bbox", pa.array(arrays.ravel()), dora_input["metadata"])
        return DoraStatus.CONTINUE