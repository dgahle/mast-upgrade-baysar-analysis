# Imports
from backend.OpenADAS import get_adf11, load_adf11, read_adf11
from numpy import array, ndarray
from xarray import DataArray


# Variables


# Functions and classes
class TestLoadAdf11:

    def test_H_ACD_yr12(self):
        adf11: str = get_adf11(element='h', adf11type='acd', year=12)
        adf11_model: DataArray = load_adf11(adf11, passed=True)
        assert type(adf11_model) is DataArray

    def test_Li_SCD_93_r(self):
        adf11: str = get_adf11(element='li', adf11type='scd', year=93, resolved=True)
        adf11_model: DataArray = load_adf11(adf11, passed=True)
        assert type(adf11_model) is DataArray

    def test_C_CCD_r(self):
        adf11: str = get_adf11(element='c', adf11type='ccd', resolved=True)
        adf11_model: DataArray = load_adf11(adf11, passed=True)
        assert type(adf11_model) is DataArray

    def test_N_QCD(self):
        adf11: str = get_adf11(element='n', adf11type='qcd')
        adf11_model: DataArray = load_adf11(adf11, passed=True)
        assert type(adf11_model) is DataArray


class TestReadAdf11:

    def test_H_ACD_yr12(self):
        ne: ndarray = array([1e13, 1e14, 1e15])
        te: ndarray = array([3, 5, 10], dtype=float)
        adf11: str = get_adf11(element='h', adf11type='acd', year=12)
        adf11_model: DataArray = read_adf11(adf11, ne=ne, te=te, passed=True)
        assert type(adf11_model) is DataArray

    def test_Li_SCD_93_r(self):
        ne: ndarray = array([1e13, 1e14, 1e15])
        te: ndarray = array([3, 5, 10], dtype=float)
        adf11: str = get_adf11(element='li', adf11type='scd', year=93, resolved=True)
        adf11_model: DataArray = read_adf11(adf11, ne=ne, te=te, passed=True)
        assert type(adf11_model) is DataArray

    def test_C_CCD_r(self):
        ne: ndarray = array([1e13, 1e14, 1e15])
        te: ndarray = array([3, 5, 10], dtype=float)
        adf11: str = get_adf11(element='c', adf11type='ccd', resolved=True)
        adf11_model: DataArray = read_adf11(adf11, ne=ne, te=te, passed=True)
        assert type(adf11_model) is DataArray

    def test_N_QCD(self):
        ne: ndarray = array([1e13, 1e14, 1e15])
        te: ndarray = array([3, 5, 10], dtype=float)
        adf11: str = get_adf11(element='n', adf11type='qcd')
        adf11_model: DataArray = read_adf11(adf11, ne=ne, te=te, passed=True)
        assert type(adf11_model) is DataArray


def main() -> None:
    pass


if __name__ == "__main__":
    main()