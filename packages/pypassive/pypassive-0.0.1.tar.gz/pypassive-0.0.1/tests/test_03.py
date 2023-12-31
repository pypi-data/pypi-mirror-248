# Description: Test calculation of various different Rankine earth pressures
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


def test_moment_arms():
    # def test_lo`g_spiral_radius_minimization():
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
    xo = 10.3195

    diff_r = lgs.calc_r(xo, w)
    lgs.calc_moment_arms(w)
    lgs.calc_Rankine_passive_earth_pressures()
    Ppphi = lgs.calc_Ppphi()
    Ppc = lgs.calc_Ppc()
    Ppq = lgs.calc_Ppq(w)
    Ep = Ppphi + Ppc + Ppq

    output = [
        np.round(lgs.Eprphi, 0),
        np.round(lgs.Eprc, 0),
        np.round(lgs.Eprq, 0),
        np.round(Ppphi, 0),
        np.round(Ppc, 0),
        np.round(Ppq, 0),
        np.round(Ep, 0),
    ]

    required_output = [1005, 7876, 0, 3471, 14343, 0, 17814]

    np.testing.assert_allclose(output, required_output, atol=1)


if __name__ == "__main__":
    main()
