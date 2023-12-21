#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dora import Node

node = Node()

for i in range(100):
    event = node.next()
    if event is not None:
        if event["type"] == "INPUT":
            if event["id"] == "image":
                print("Got image", event["data"])
