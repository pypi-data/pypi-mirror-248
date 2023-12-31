# Description: Test calculation of log spiral r, by minimizing the difference between the diagonal
# distance to the end of the log spiral and the log spiral radius to the same point.
# ref: Mokwa, R. L. (1999). Investigation of Resistance of Pile Caps to Lateral Loading.
# Appendix F, pg. 359 -- 372

import numpy as np
from scipy.optimize import minimize_scalar
from pypassive import (
    SoilLayer,
    RetainingWall,
    DuncanMokwaLogSpiral,
)


def test_log_spiral_radius_minimization():
    # soil parameters
    # Mohr-Coulomb c parameter [psf], cohesion
    c = 970
    # Mohr-Coulomb phi parameter [deg], friction angle
    phi = 37
    # unit weight of the soil, [pcf]
    gamma = 122
    # soil-structure interface angle [deg]
    delta = 3.5
    # Young's modulus of the soil layer [psf]
    modE = 890000
    # Poisson's ratio of the soil layer [-]
    nu = 0.33
    # adhesion ratio between the soil and the wall [-] range 0 -- 1 adhesion = alphac * c
    alphac = 0
    # surchage on top of the wall [psf]
    q = 0
    # foundation parameters
    # foundation/wall height [ft]
    h = 3.5
    # foundation width [ft]
    b = 6.3

    sl = SoilLayer(c, phi, gamma, delta, modE, nu, alphac, q)
    rw = RetainingWall(h, b)

    lgs = DuncanMokwaLogSpiral(sl, rw)

    # width of the log spiral extent on the surface
    w = 4.0604
    bnds = (-5.0 * h, 5 * h)

    res = minimize_scalar(
        lgs.calc_r,
        args=(w),
        bounds=bnds,
        method="bounded",
    )

    output = [
        np.round(lgs.xo, 2),
        np.round(lgs.yo, 2),
        np.round(lgs.theta, 3),
        np.round(lgs.r, 4),
    ]

    required_output = [10.32, 5.15, 0.235, 16.0680]

    np.testing.assert_allclose(output, required_output, rtol=0.00005)
