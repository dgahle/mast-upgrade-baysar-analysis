# Imports
from backend import get_logger
from numpy import array, diag, load, ndarray, square, trapz, zeros
from numpy.random import multivariate_normal
from pathlib import Path
from scipy.constants import pi


# Variables
script_name: str = Path(__file__).name
logger = get_logger(script_name)
data_path: Path = Path(__file__).parent.parent.parent / "input" / "simple-c-ii-analysis" / "46578_1.npy"


# Functions and classes
def get_posterior_distribution() -> ndarray:
    mean: ndarray = array([
        1.5e13,  # electron density (cm-3)
        2.5,  # electron temperature (eV)
        4,  # emission path length (cm)
    ])
    cov: ndarray = diag(
        array([
            0.5e13,  # electron density (cm-3)
            0.5,  # electron temperature (eV)
            1,  # emission path length (cm)
        ])
    )
    sample_size: int = 100
    sample: ndarray = multivariate_normal(mean, cov, size=sample_size)

    return sample


def calculate_tec_sample(electron_density: ndarray, electron_temperature: ndarray) -> ndarray:
    logger.warning('Not implemented properly all TECs = 1.')
    # logger.info('Evaluate ionisation balance')
    # logger.info('Evaluate PECs')
    # total_emission_coefficient: ndarray = electron_temperature * (
    #     f_exc * pec_excitation + f_rec * pec_recombination
    # )
    total_emission_coefficient: ndarray = 1. + zeros(electron_density.shape)
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
    min_wavelength: float = 433.5
    max_wavelength: float = 434.5
    lhs_index: int = square(wavelength[20] - min_wavelength).argmin()
    rhs_index: int = square(wavelength[20] - max_wavelength).argmin()
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
