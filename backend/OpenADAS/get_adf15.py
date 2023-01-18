#
#
#
#
#
# Imports
from backend import get_logger
from numpy import array, ndarray, where
from urllib import request
from pathlib import Path


# Variables
logger = get_logger(Path(__file__).name)


# Functions
def get_adf15(
        element: str,
        charge: int,
        year: int = 96,
        resolved: bool = False,
        visible: bool = True
    ) -> None:
    """
    Download OpenADAS ADF15 library.


    :return:
    """
    # Format inputs
    resolution: str = 'r' if resolved else 'u'
    visible: str = 'vs' if visible else 'pj'
    # Construct the download URL
    download_url: str = f'https://open.adas.ac.uk/download/adf15/pec{year}][{element}/pec{year}][{element}_{visible}{resolution}][{element}{charge}.dat'
    # Download
    with request.urlopen(download_url) as f:
        _: str = f.read().decode('utf-8')

    pass


def main() -> None:
    pass

if __name__ == "__main__":
    main()
