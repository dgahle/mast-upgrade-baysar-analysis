#
#
#
#
#
# Imports
from urllib import request


# Variables



# Functions
def get_adf11(
        element: str,
        adf11type: str,
        year: int = 96,
        resolved: bool = False
    ) -> None:
    """
    Download OpenADAS ADF11 library.


    :return:
    """
    # Format inputs
    resolution: str = 'r' if resolved else ''
    adf11type = f'{adf11type}{year}{resolution}'
    # Construct the download URL
    download_url: str = f'https://open.adas.ac.uk/download/adf11/{adf11type}_{adf11type}{element}.dat'
    # Download
    with request.urlopen(download_url) as f:
        _: str = f.read().decode('utf-8')

    pass


def main() -> None:
    pass


if __name__ == "__main__":
    main()
