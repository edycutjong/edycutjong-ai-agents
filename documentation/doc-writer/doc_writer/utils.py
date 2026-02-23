import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme
from .config import config

# Premium UI Theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "code": "italic white"
})

console = Console(theme=custom_theme)

def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    # Force reconfiguration
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )
    return logging.getLogger("doc-writer")

# Initialize logger with config setting
logger = setup_logging(verbose=config.VERBOSE)
