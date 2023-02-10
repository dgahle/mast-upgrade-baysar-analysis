# Imports 1


# Variables


# Functions and classes
def _adf_exists_check(adf15: str, download_url: str) -> None:
    """
    Checks that an adf15 was downloaded.

    :param (str) adf15:
        The adf15 file downloaded from OpenADAS.
    :param (str) download_url:
        OpenADAS URL to download the adf15

    :return: None

    :raise ValueError:
        No adf15 downloaded.
    """
    if 'OPEN-ADAS Error' in adf15:
        # Extract adf15 file name from url
        adf15_name: str = '#'.join(download_url.split('][')[1:]).split('/')[1]
        # Write error message and raise error
        err_msg: str = f"No ADF15 was downloaded, '{adf15_name}' does not exist (url: '{download_url}')!"
        raise ValueError(err_msg)


def main() -> None:
    pass


if __name__=="__main__":
    main()
    