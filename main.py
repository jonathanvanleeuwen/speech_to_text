import logging
import time
import os
from datetime import timedelta
from pathlib import Path

import argh
from dotenv import load_dotenv

from src.entry import run_code
from src.about import version

logger = logging.getLogger()
load_dotenv()


def config_logger() -> None:
    """
    Define the settings for the logger
    """
    log_file = Path("template_log.log")
    log_file.unlink(missing_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


@argh.arg("--language", help="The language used (default 'en-US')")
@argh.arg("--max_duration", help="The max duration the service will continue before trying to close (seconds)")
@argh.arg("--out", help="Filepath to .txt file to save results!")
@argh.arg("--filepath", help="Filepath to .wav file to run speech to text on!")
def entry(filepath: Path = None, out: Path = None, max_duration: int = None, language: str = "en-US") -> None:
    """
    Information about the entry point
    """
    config_logger()
    start = time.time()
    if filepath is not None:
        filepath = Path(filepath)
    if out is not None:
        out = Path(out)
    options = {"filepath": filepath, "out": out, "max_duration": max_duration, "language": language}
    sepperator = "_" * 120
    logger.info(sepperator)
    logger.info("Starting speech to text:")
    logger.info(sepperator)
    logger.info(f"Settings: {options}")
    logger.info(sepperator)
    options["subscription"] = os.environ.get("SUBSCRIPTION")
    run_code(options)
    logger.info(sepperator)
    logger.info("Done!")
    logger.debug(f"Duration: {str(timedelta(seconds=int(time.time()-start)))}")


if __name__ == "__main__":
    argh.dispatch_commands([entry, version])
