#
#
#
#
#
# Imports
from numpy import arange, array, ceil, ndarray, power
from pathlib import Path
from xarray import DataArray


# Variables
ADAS_PATH: Path = Path(__file__).parent.parent / 'adas'
Adf11_SEPARATOR: str = 'C-----------------------------------------------------------------------'


# Functions
def get_number_of_blocks(adf11_raw: str) -> int:
    header: str = adf11_raw.split('\n')[0]
    total_blocks: int = int(
        header.split()[0]
    )
    return total_blocks


def block_str_to_array(adf11_block: list) -> DataArray:
    header: list = adf11_block[0].split()
    num_ne_index: int = 2 if header[1] == 'A' else 1
    num_te_index: int = 3 if header[1] == 'A' else 2
    num_ne: int = int(header[num_ne_index])
    num_te: int = int(header[num_te_index])
    pecs: str = ' '.join(adf11_block[1:])
    pecs: ndarray = array([float(p) for p in pecs.split()])
    ne_slice: slice = slice(0, num_ne)
    te_slice: slice = slice(num_ne, num_ne + num_te)
    ne: ndarray = pecs[ne_slice]
    te: ndarray = pecs[te_slice]
    pecs: ndarray = pecs[te_slice.stop:].reshape((num_ne, num_te))
    # dims: tuple = ('ne / cm-3', 'Te / eV')
    dims: tuple = ('ne', 'Te')
    coords: dict = dict(
        ne=ne,
        Te=te
    )
    attrs: dict = dict(
        description=adf11_block[0],
        units='cm3/s'
    )
    block_array: DataArray = DataArray(pecs, dims=dims, coords=coords, name='pecs', attrs=attrs)
    return block_array


def block_start_check(line: str) -> bool:
    checks: list = [
        'EXCIT', 'RECOM', 'CHEXC', 'TYPE', 'type'
    ]
    checks: list = [ch in line for ch in checks]
    check: int = sum(checks)
    check: bool = True if check == 2 else False
    return check


def get_header_slice(adf11_raw: str) -> int:
    adf11: list = adf11_raw.split('\n')
    i: int
    line: str
    for i, line in enumerate(adf11):
        if block_start_check(line):
            return i
    else:
        raise ValueError('No line found!')


def build_adf11_dataarray(adf11_raw: str) -> DataArray:
    # Get the data shape (block, ne, Te)
    data_shape: tuple = tuple(int(n) for n in adf11_raw.split('\n')[0].split()[:3])
    # Get the (ne, Te) grid
    flat_grid: ndarray = array(
        [
            float(n) for n in [s for s in adf11_raw.split('---') if s != ''][1].split()[1:]
        ]
    )
    ne: ndarray = flat_grid[:data_shape[1]]
    te: ndarray = flat_grid[data_shape[1]:]
    # Get the number of lines in each block
    start_block: int = 9
    len_block: int = int(
        ceil(data_shape[1] * data_shape[2] / 8)
    )
    # Extract rates
    rates: list = []
    block: int
    for block in range(data_shape[0]):
        # Calculate lines of adf11 to extract
        # block += 1
        lhs: int = 1 + start_block + block * (1 + len_block)
        rhs: int = lhs + len_block
        index: slice = slice(lhs, rhs)
        # Extract and format rates
        _rates: list = adf11_raw.split('\n')[index]
        _rates: str = " ".join(_rates)
        _rates: ndarray = array(
            [float(r) for r in _rates.split()]
        )
        _rates = _rates.reshape(data_shape[1:][::-1]).T
        rates.append(_rates)
    # Format rates to build DataArray
    rates: ndarray = array(rates)
    dims: tuple = ('block', 'ne', 'Te')
    coords: dict = dict(
        block=1 + arange(data_shape[0]),
        ne=ne,
        Te=te
    )
    attrs: dict = dict(
        description='TBC',  # Adf11_SEPARATOR.join(adf11_raw_list[1:]),
        units='cm3/s',
        adf=adf11_raw
    )
    data_adf11: DataArray = DataArray(
        rates,
        dims=dims,
        coords=coords,
        name='pecs',
        attrs=attrs
    )

    from matplotlib.pyplot import show
    data_adf11.isel(block=0).plot()  # .show()
    show()

    return data_adf11


def load_adf11(adf11: [str, Path], passed: bool = False) -> DataArray:
    # Load as text file
    if not passed:
        with open(adf11, 'r') as f:
            adf11_raw: str = f.read()
    else:
        adf11_raw: str = adf11
    # Separate by block nuber
    adf11_model: DataArray = build_adf11_dataarray(adf11_raw)
    return adf11_model


def read_adf11(adf11: [str, Path],
               block: [int, list],
               ne: ndarray,
               te: ndarray,
               passed: bool = False) -> DataArray:
    """
    Reads ADAS formatted Adf11 (PEC files) and returns

    :param adf11:
    :param block:
    :param te:
    :param ne:
    :return:
    """
    # Load DataArray
    adf11_model: DataArray = load_adf11(adf11, passed=passed)
    # Interpolate to get desired values
    block: list = [block] if type(block) is int else block
    kwargs: dict = dict(fill_value="extrapolate")
    pecs_out: DataArray = adf11_model.interp(block=block, ne=ne, Te=te, kwargs=kwargs)
    return pecs_out


def main() -> None:
    pass


if __name__ == "__main__":
    main()
    