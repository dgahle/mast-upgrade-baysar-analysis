# Imports
from backend.OpenADAS import get_adf15


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


def main() -> None:
    pass


if __name__ == "__main__":
    main()
