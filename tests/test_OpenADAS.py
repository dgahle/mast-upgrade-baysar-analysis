# Imports
from backend.OpenADAS import get_adf15, list_adf15s


# Variables


# Functions and classes
class TestGetAdf15:

    def test_C_III(self):
        element: str = 'c'
        charge: int = 2
        get_adf15(element, charge)
        assert True

    def test_Ne_III(self):
        element: str = 'ne'
        charge: int = 2
        get_adf15(element, charge)
        assert True

    def test_H_I(self):
        element: str = 'h'
        charge: int = 0
        get_adf15(element, charge, year=12)
        assert True


class TestListAdf15s:

    def test_one(self):
        list_adf15s(element='c')
        assert True

    def test_two(self):
        list_adf15s(element='n', charge=4)
        assert True

    def test_three(self):
        list_adf15s(element='ar', charge=3, wave_min=10, wave_max=2000)
        assert True


def main() -> None:
    pass


if __name__ == "__main__":
    main()
