# Imports
from backend import get_logger, read_adf15
from numpy import array, diag, load, ndarray, square, trapz, zeros
from numpy.random import multivariate_normal
from pathlib import Path
from scipy.constants import pi
from xarray import DataArray


# Variables
script_name: str = Path(__file__).name
logger = get_logger(script_name)
REPO_PATH: Path = Path(__file__).parent.parent.parent
C_II_ADF15_PATH: Path = REPO_PATH / "Open-ADAS" / "pec96#c_vsu#c1.dat"
data_path: Path = REPO_PATH / "input" / "simple-c-ii-analysis" / "46860_1.npy"


# Functions and classes
def get_posterior_distribution() -> ndarray:
    mean: ndarray = array([
        1.5,  # electron density (in 1e13 cm-3)
        5,  # electron temperature (eV)
        4,  # emission path length (cm)
    ])
    cov: ndarray = diag(
        array([
            0.5,  # electron density (in 1e13 cm-3)
            1,  # electron temperature (eV)
            1,  # emission path length (cm)
        ])
    )
    sample_size: int = 100
    sample: ndarray = multivariate_normal(mean, cov, size=sample_size)
    sample[:,0] = sample[:,0]*1e13 # convert to cm-3

    return sample


def calculate_tec_sample(electron_density: ndarray, electron_temperature: ndarray) -> ndarray:
    logger.warning('No ionisation balance - providing only concentration of analysed charged ion.')
    # logger.info('Evaluate ionisation balance')
    logger.info('Evaluate PECs')
    blocks: list = [24, 74]
    pecs: DataArray = read_adf15(C_II_ADF15_PATH, block=blocks, ne=electron_density, te=electron_temperature)
    pecs: ndarray = pecs.data.mean(1)  # (block, duplicate, sample)
    pecs_exc, pecs_rec = pecs
    # total_emission_coefficient: ndarray = electron_temperature * (
    #     f_exc * pec_excitation + f_rec * pec_recombination
    # )
    #total_emission_coefficient: ndarray = electron_density * 0.5 * (pecs_exc + pecs_rec)
    total_emission_coefficient: ndarray = electron_density * pecs_exc
    return total_emission_coefficient


def load_emission() -> ndarray:
    data: dict = load(str(data_path), allow_pickle=True)[()]
    """
    emission.keys()
    dict_keys(['wavelength', 'spectra_counts', 'time', 'settings', 'spectra_abs', 'shotnr'])
    emission['wavelength'].shape
    (40, 1024)
    """
    emission: ndarray = data['spectra_abs']  # (time, chords, pixel)
    wavelength: ndarray = data['wavelength']  # (chords, pixel)
    # Filter by wavelength
    min_wavelength: float = 426.3
    max_wavelength: float = 426.9
    lhs_index: int = square(wavelength[0,:] - min_wavelength).argmin()
    rhs_index: int = square(wavelength[0,:] - max_wavelength).argmin()
    wavelength_check: slice = slice(lhs_index, rhs_index)
    emission = emission[:, :, wavelength_check]
    wavelength = wavelength[:, wavelength_check]
    # Integrate "ph / m2 / nm / sr / s" -> "ph / m2 / sr / s"
    emission = trapz(emission, wavelength)
    # Unit conversion "ph / m2 / sr / s" -> "ph / cm2 / sr / s"
    emission /= square(100.)
    return emission


def main() -> None:
    logger.info('Building parameter posterior distribution')
    sample: ndarray = get_posterior_distribution()
    electron_density, electron_temperature, path_length = sample.T
    logger.info('Calculate TEC')
    total_emission_coefficient: ndarray = calculate_tec_sample(electron_density, electron_temperature)
    logger.info('Get C II emission')
    emission = load_emission()
    logger.info('Calculate carbon concentration!')
    concentration: ndarray = 4 * pi * emission[:, :, None] / (path_length * electron_density * total_emission_coefficient)
    # TODO: Need to format and save using xarray
    logger.info('Completed main!')
    pass


if __name__ == "__main__":
    main()
