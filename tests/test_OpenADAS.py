# Imports
from backend.OpenADAS import get_adf11, get_adf15, list_adf15s


# Variables


# Functions and classes
class TestGetAdf11:

    def test_one(self) -> None:
        adf11: str = get_adf11(element='h', adf11type='acd', year=12)
        assert type(adf11) is str

    def test_two(self) -> None:
        adf11: str = get_adf11(element='li', adf11type='scd', year=93, resolved=True)
        assert type(adf11) is str

    def test_three(self) -> None:
        adf11: str = get_adf11(element='c', adf11type='ccd', resolved=True)
        assert type(adf11) is str

    def test_four(self) -> None:
        adf11: str = get_adf11(element='n', adf11type='scd')
        assert type(adf11) is str


class TestGetAdf15:

    def test_C_III(self):
        adf15: str = get_adf15(element='c', charge=2)
        assert type(adf15) is str

    def test_Ne_III(self):
        adf15: str = get_adf15(element='ne', charge=2)
        assert type(adf15) is str

    def test_H_I(self):
        adf15: str = get_adf15(element='h', charge=0, year=12)
        assert type(adf15) is str


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
