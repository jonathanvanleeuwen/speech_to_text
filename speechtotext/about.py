__title__ = "speech-to-text-az-interface"
__description__ = "A simple speech to text interface for Azure speech to text"

__version__ = "0.0.2"

__author__ = "Jonathan van Leeuwen"
__email__ = "jonathan89j@hotmail.com"

__release_notes__ = f"\n{'-'*120}\n".join(
    [
        "0.0.1 - Release notes\nInitial setup",
        "0.0.2 - Updated format for better packaging",
    ]
)


def version() -> None:
    """
    Print version information
    """
    sepperator = "*" * 120
    joiner = f"\n{'-'*120}\n"
    release_notes = joiner.join(__release_notes__.split(joiner)[::-1])
    print(sepperator)
    print(f"Release notes:\n{release_notes}")
    print(sepperator)
    print(f"Title:\n\t{__title__}")
    print(sepperator)
    print(f"Summary:\n\t{__description__}")
    print(sepperator)
    print(f"Version:\n\t{__version__}")
    print(sepperator)
    print(f"Author:\n\t{__author__}")
    print(sepperator)
    print(f"Email:\n\t{__email__}")
    print(sepperator)
