import logging
import time
from pathlib import Path
from typing import Union

import azure.cognitiveservices.speech as speechsdk

logger = logging.getLogger()


class SpeechToText:
    """
    Class which can be used to interface with azure speech to text service

    required kwargs:
    :param subscription: The subscription key to use for the service, str

    optional kwargs
    :param region: The region of the service i.e. westeurope (default), str
    :param out: The output file and location to save results i.e. "./default_out.txt" (default), Path
    :param max_duration: The maximum time the recognizer will run, seconds i.e. 60 (default), Int
    :param language: The language the recognizer will use, i.e. "en-US" (default), str
    """

    def __init__(self, **kwargs):
        self.subscription = kwargs.get("subscription")
        self.region = kwargs.get("region", "westeurope")
        self.out = kwargs.get("out", None)
        self.max_duration = kwargs.get("max_duration", None)
        if self.max_duration is None:
            self.max_duration = 60
        else:
            self.max_duration = int(self.max_duration)
        if self.out is None:
            self.out = Path("./default_out.txt")
        self.done = False
        self._sepperator = "_" * 120
        self.speech_config = speechsdk.SpeechConfig(subscription=self.subscription, region=self.region)
        self.speech_config.speech_recognition_language = kwargs.get("language", "en-US")
        self.speech_recognizer: Union[speechsdk.SpeechRecognizer, None] = None

    def set_out(self, out: Path) -> None:
        self.out = out

    def from_file(self, filepath: Path) -> None:
        self.done = False
        logger.info(f"Running speech to text from file: {filepath.resolve()}")
        audio_input = speechsdk.AudioConfig(filename=str(filepath.resolve()))
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_input)
        self._start_recognition()

    def from_mic(self) -> None:
        self.done = False
        logger.info("Running speech to text from microphone!")
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
        self._start_recognition()

    def _start_recognition(self) -> None:
        self.speech_recognizer.recognized.connect(self._save_to_file)
        # self.speech_recognizer.recognized.connect(lambda evt: self._save_to_file((evt)))
        self.speech_recognizer.session_stopped.connect(self._stop_cb)
        logger.info("Starting continuous recognition")
        self.speech_recognizer.start_continuous_recognition()
        self.start = time.time()
        try:
            while not self.done and time.time()-self.start < self.max_duration:
                time.sleep(.5)
        except KeyboardInterrupt:
            logger.info(self._sepperator)
            logger.info("Stopped by user")
        logger.info(self._sepperator)
        logger.info("Finished or timed out, please wait!")
        self._stop_cb()
        self.done = True

    def _save_to_file(self, resultEvent: speechsdk.SpeechRecognitionEventArgs, out: Union[Path, None] = None) -> None:
        if out is None:
            out = self.out
        out = str(out.resolve())
        logger.debug(f"Saving results to: {out}")
        logger.debug(f"----{resultEvent.result.text}")
        with open(out, "a") as f:
            f.write(resultEvent.result.text)
            f.write("\n")

    def _stop_cb(self, evt: Union[str, None] = None):
        self.speech_recognizer.stop_continuous_recognition()
        if self.done is False:
            logger.info("Stopping continuous recognition!")
        self.done = True
