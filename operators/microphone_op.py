# Run this in the consol first :

# pip install sounddevice numpy

# Don't forget to install whisper

import time

import numpy as np
import pyarrow as pa
import sounddevice as sd
from typing import Callable, Optional, Union
from dora import DoraStatus

# Set the parameters for recording
SAMPLE_RATE = 16000
MAX_DURATION = 5
MAX_DURATION_LONG = 12


class Operator:
    """
    Infering object from images
    """

    def __init__(self):
        pass

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
        if dora_input["id"] == "mic_on":
            audio_data = sd.rec(
                int(SAMPLE_RATE * MAX_DURATION),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype=np.int16,
                blocking=False,
            )
            time.sleep(MAX_DURATION)

            audio_data = audio_data.ravel().astype(np.float32) / 32768.0
            if len(audio_data) > 0:
                send_output("audio", pa.array(audio_data), dora_input["metadata"])

        elif dora_input["id"] == "mic_on_long":
            audio_data = sd.rec(
                int(SAMPLE_RATE * MAX_DURATION_LONG),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype=np.int16,
                blocking=False,
            )
            time.sleep(MAX_DURATION_LONG)

            audio_data = audio_data.ravel().astype(np.float32) / 32768.0
            if len(audio_data) > 0:
                send_output("audio", pa.array(audio_data), dora_input["metadata"])
        return DoraStatus.CONTINUE
