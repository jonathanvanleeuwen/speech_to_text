import logging
import time
import traceback

import azure.cognitiveservices.speech as speechsdk
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


def set_logging_level(level: str) -> None:
    if logger.hasHandlers() is False:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(level)


class SpeechToText:
    """
    Class which can be used to interface with azure speech to text service

    required kwargs:
    :param subscription: The subscription key to use for the service, str

    optional kwargs
    :param region: The region of the service i.e. westeurope (default), str
    :param out: The output file and location to save results i.e. "./default_out.txt" (default), Path
    :param max_duration: The maximum time the recognizer will run, seconds i.e. 3600 (default), Int
    :param language: The language the recognizer will use, i.e. "en-US" (default), str
    :param verbose: logging level to output, default = INFO
    """

    def __init__(self, **kwargs):
        self.subscription = kwargs.get("subscription")
        self.region = kwargs.get("region", "westeurope")
        self.out = kwargs.get("out", None)
        self.max_duration = kwargs.get("max_duration", None)
        self.verbose = kwargs.get("verbose", "INFO")
        set_logging_level(self.verbose)
        if self.max_duration is None:
            self.max_duration = 3600
        else:
            self.max_duration = int(self.max_duration)
        if self.out is None:
            self.out = Path("./default_out.txt")
        self._done = False
        self._initated = False
        self._sepperator = "_" * 120
        try:
            self.speech_recognizer: Union[speechsdk.SpeechRecognizer, None] = None
            self.speech_config = speechsdk.SpeechConfig(subscription=self.subscription, region=self.region)
            self.speech_config.speech_recognition_language = kwargs.get("language", "en-US")
            self._initated = True
        except (RuntimeError, ValueError) as e:
            logger.error(e)
            logger.error("Unable to connect to Azure service")
            logger.error("".join(traceback.format_exception(type(e), e, e.__traceback__)))
            self._done = True

    def from_file(self, filepath: Path) -> None:
        self._done = False
        if self._initated:
            logger.info(f"Running speech to text from file: {filepath.resolve()}")
            audio_input = speechsdk.AudioConfig(filename=str(filepath.resolve()))
            self.speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config, audio_config=audio_input
            )
            self._start_recognition()
        else:
            logger.error("Instance not connected to Azure")

    def from_mic(self) -> None:
        self._done = False
        if self._initated:
            logger.info("Running speech to text from microphone!")
            self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
            self._start_recognition()
        else:
            logger.error("Instance not connected to Azure")

    def _start_recognition(self) -> None:
        self.speech_recognizer.recognized.connect(self._save_to_file)
        # self.speech_recognizer.recognized.connect(lambda evt: self._save_to_file((evt)))
        self.speech_recognizer.session_stopped.connect(self._stop_cb)
        logger.info("Starting continuous recognition")
        self.speech_recognizer.start_continuous_recognition()
        self.start = time.time()
        try:
            while not self._done and time.time() - self.start < self.max_duration:
                time.sleep(0.5)
        except KeyboardInterrupt:
            logger.info(self._sepperator)
            logger.info("Stopped by user")
        logger.info(self._sepperator)
        logger.info("Finished or timed out, please wait!")
        self._stop_cb()
        self._done = True

    def _save_to_file(self, resultEvent: speechsdk.SpeechRecognitionEventArgs, out: Union[Path, None] = None) -> None:
        if out is None:
            out = self.out
        out = str(out.resolve())
        logger.info(f"Saving results to: {out}")
        logger.info(f"----{resultEvent.result.text}")
        with open(out, "a") as f:
            f.write(resultEvent.result.text)
            f.write("\n")

    def _stop_cb(self, evt: Union[str, None] = None):
        self.speech_recognizer.stop_continuous_recognition()
        if self._done is False:
            logger.info("Stopping continuous recognition!")
        self._done = True
