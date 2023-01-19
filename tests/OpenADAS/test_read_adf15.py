# Imports
from backend.OpenADAS import get_adf15, load_adf15
from xarray import DataArray

# Variables


# Functions and classes
class TestLoadAdf15:

    def test_C_III(self):
        adf15: str = get_adf15(element='c', charge=2)
        adf15_model: DataArray = load_adf15(adf15, passed=True)
        assert type(adf15_model) is DataArray

    def test_N_II(self):
        adf15: str = get_adf15(element='n', charge=1)
        adf15_model: DataArray = load_adf15(adf15, passed=True)
        assert type(adf15_model) is DataArray

    def test_Ne_III(self):
        adf15: str = get_adf15(element='ne', charge=2)
        adf15_model: DataArray = load_adf15(adf15, passed=True)
        assert type(adf15_model) is DataArray

    def test_H_I(self):
        adf15: str = get_adf15(element='h', charge=0, year=12)
        adf15_model: DataArray = load_adf15(adf15, passed=True)
        assert type(adf15_model) is DataArray


def main() -> None:
    pass


if __name__ == "__main__":
    main()
