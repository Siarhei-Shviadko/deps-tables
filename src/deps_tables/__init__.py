import logging

from deps_tables.settings import Settings

logging.basicConfig(
    level=Settings().logger_level.upper(),
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S",
)
