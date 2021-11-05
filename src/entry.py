import logging
from typing import Dict

from src.speech_to_text.speech_to_text import SpeechToText

logger = logging.getLogger()


def run_code(options: Dict) -> None:
    """
    Main executing code for the project.
    """
    speech_recognizer = SpeechToText(**options)
    if options["filepath"] is not None:
        speech_recognizer.from_file(options["filepath"])
    else:
        speech_recognizer.from_mic()
