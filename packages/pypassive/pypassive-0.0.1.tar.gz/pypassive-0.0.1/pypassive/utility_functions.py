import numpy as np


def ovesen_3D_effects_correction(
    phi: float, width: float, height: float, depth: float, spacing: float
):
    """Ovesen-Brinch Hansen Method of correcting for 3D Effects in Passive Earth Pressures.

    :param float phi: Mohr-Coulomb phi parameter, soil friction angle, degrees
    :param float width: Width of the foundation/retaining wall.
    :param float height: Height of the foundation/retaining wall.
    :param float depth: Distance from the top of the soil layer to the top of the foundation/retaining wall.
    :param float spacing: If multiple close-by footing or retaining wall

    """
    phi = np.radians(phi)
    ka = np.tan(np.pi / 4 - phi / 2) ** 2
    kp = np.tan(np.pi / 4 + phi / 2) ** 2
    fac_b = 1 - (width / spacing) ** 2
    fac_e = 1 - height / (depth + height)
    return 1 + (kp - ka) ** 0.67 * (
        1.1 * fac_e**4
        + 1.6 * fac_b / (1 + 5 * (width / height))
        + 0.4 * (kp - ka) * fac_e**3 * fac_b**2 / (1 + 0.05 * (width / height))
    )


def rankine_passive_pressure_coeff(phi: float, c: float) -> float:
    """Compute Rankine earth pressure coefficient.
    Use consistent units
    :param phi: Mohr-Column phi parameter, friction angle in degrees
    :type: float
    :param c: Mohr-Column c parameter, cohesion in F/L^2
    :type: float
    :param height: wall height in units of length, L
    :type: float
    :param gamma: unit weight of the soil in F/L^3
    :type: float
    :return: kp, coefficient of passive earth pressure
    :rtype: float
    """

    return np.tan(np.pi / 4 + np.radians(phi) / 2) ** 2
