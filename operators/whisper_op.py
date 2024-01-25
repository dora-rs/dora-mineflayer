# Run this in the consol first :

# pip install sounddevice numpy scipy pydub keyboard

# Don't forget to install whisper


import pyarrow as pa
import whisper

from typing import Callable, Optional, Union
from dora import DoraStatus

model = whisper.load_model("base")

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
        if dora_input["id"] == "audio":
            audio = dora_input["value"].to_numpy()
            audio = whisper.pad_or_trim(audio)

            ## make log-Mel spectrogram and move to the same device as the model
            # mel = whisper.log_mel_spectrogram(audio).to(model.device)

            ## decode the audio
            # result = whisper.decode(model, mel, options)
            result = model.transcribe(audio, language="en")
            text = result["text"]
            text = text.lower()
            if "please" in text: #change this to whatever you want to trigger the output
                send_output("please", pa.array([text]), dora_input["metadata"])
            else:
                send_output("text", pa.array([text]), dora_input["metadata"])
            #this will write the text to a file
            #with open('readme.txt', 'w') as f:
            #    f.write(text)
            
        return DoraStatus.CONTINUE
