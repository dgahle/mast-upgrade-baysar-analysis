#
#
#
#
#
# Imports
from numpy import array, ndarray, where
from pathlib import Path
from pandas import DataFrame
from urllib import request


# Variables



# Functions
def str_strip(string: str, remove: [str, list]) -> str:
    remove: list = [remove] if type(remove) is str else remove
    _remove: str
    for _remove in remove:
        string = string.replace(_remove, '')
    return string


def format_list_adf15s_input(variable) -> str:
    return '' if variable is None else f'{variable}'


def get_adf15_query_url(
        element: str,
        charge: int = None,
        wave_min: float = None,
        wave_max: float = None,
        resolveby: str = 'file'
    ) -> str:
    # Format inputs
    charge: str = format_list_adf15s_input(charge)
    wave_min: str = format_list_adf15s_input(wave_min)
    wave_max: str = format_list_adf15s_input(wave_max)
    # Produce OpenADAS query url
    url: str = "https://open.adas.ac.uk/adf15?" \
               f"element={element}&" \
               f"charge={charge}&" \
               f"wave_min={wave_min}&" \
               f"wave_max={wave_max}&" \
               f"resolveby={resolveby}&" \
               "searching=1"
    return url


def check_for_results_table(html: str, url: str) -> None:
    str_check: str = '\t<div id="searchresults">'
    if not str_check in html:
        details: str = ', '.join(
            url[30:] \
                .replace('&', ', ') \
                .replace('=', ' = ') \
                .split(', ')[:-2]
        )
        error_msg: str = "Your OpenADAS query returned no ADF15 files!\n" \
                         f"{4 * ' '}Query details: {details}."
        raise ValueError(error_msg)


def extract_html_results_table(html: str) -> str:
    # Preprocess HTML
    html: ndarray = array(html.split('\n'), dtype=str)
    # Find the lines of the HTML that contain the results table
    start_line: str = '        \t<div id="searchresults">'
    end_line: str = '        \t</div>'
    start: int = where(html == start_line)[0][0]
    end: int = where(html == end_line)[0][0]
    # Get table from the HTML
    table_slice: slice = slice(start, end)
    table: ndarray = html[table_slice][-1].strip().split('<tr>')

    return table


def format_dataframe(df: DataFrame) -> DataFrame:
    df['Ion'] = df['Ion'].apply(
        lambda x: str_strip(x, [' ', '<td>', '<sup>', '</sup>'])
    )
    col: str = 'Minimum Wavelength / A'
    df[col] = df[col].apply(
        lambda x: str_strip(x, [' ', '<td>', '&Aring;'])
    )
    col: str = 'Maximum Wavelength / A'
    df[col] = df[col].apply(
        lambda x: str_strip(x, [' ', '<td>', '&Aring;'])
    )
    col: str = 'adf15'
    df[col] = df[col].apply(
        lambda x: x.split(' ')[-1][:-4]
    )
    return df


def list_adf15s(
        element: str,
        charge: int = None,
        wave_min: float = None,
        wave_max: float = None,
        resolveby: str = 'file'
    ) -> None:
    """
    Query OpenADAS ADF15 library and prints the available adf15 files

    :return:
    """
    # Produce OpenADAS query url
    url: str = get_adf15_query_url(
        element,
        charge,
        wave_min,
        wave_max,
        resolveby
    )
    # Query OpenADAS
    with request.urlopen(url) as f:
        html: list = f.read().decode('utf-8')
    # Check that results exist!
    check_for_results_table(html, url)
    # Preprocess search results
    table: str = extract_html_results_table(html)
    # Format the table into a DataFrame
    data: ndarray = array(
        [line.split('</td>')[:-1] for line in table[2:]],
        dtype=str
    )
    columns: list = ["Ion",	"Minimum Wavelength / A", "Maximum Wavelength / A", "adf15"]
    df: DataFrame = DataFrame(data, columns=columns)
    # Format DataFrame to be human-readable
    df = format_dataframe(df)
    # Print/return
    print(df)
    pass


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
