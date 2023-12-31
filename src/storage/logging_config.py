import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="./src/storage/files/logs.log",
    filemode="a"
)


logger = logging.getLogger("default_logger")

# Console handler for testing purpose! Remove in production
"""
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
"""
