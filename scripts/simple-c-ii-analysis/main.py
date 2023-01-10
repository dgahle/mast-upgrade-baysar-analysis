# Imports
from backend import get_logger
from pathlib import Path


# Variables
script_name: str = Path(__file__).name
logger = get_logger(script_name, set_path=False)


# Functions and classes
def main() -> None:
    logger.info('Building parameter posterior distribution')
    logger.info('Evaluate ionisation balance')
    logger.info('Evaluate PECs')
    logger.debug('Calculate TEC')
    logger.info('Get C II emission')
    logger.info('Calculate carbon concentration!')
    logger.info('Completed main!')
    pass


if __name__ == "__main__":
    main()
