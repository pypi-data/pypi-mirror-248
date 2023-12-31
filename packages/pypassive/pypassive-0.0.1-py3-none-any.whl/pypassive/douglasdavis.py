import numpy as np
from typing import Any, Tuple


class DouglasDavis1964:
    """Deflection at upper (y1) and lower (y2) corners of the horizontally loaded rectangular area

    Elasticity solution for horizontal loading on a vertical rectangle.
    Douglas, D. J., and Davis, E. H. (1964). Geotechnique Vol. 14(3), p 115-132

    :param float load: Total horizontal load on the rectangular area
    :returns Tuple(): A tuple of floats of corner deflections.

    """

    def __init__(self, soillayer, foundation) -> None:
        self._modE = soillayer.modE
        self._nu = soillayer.nu
        self._q = soillayer.q
        self._gamma = soillayer.gamma
        self._h = foundation.h
        self._b = foundation.b
        self._z = foundation.z
        self._influence_factors = self.calc_influence_factors()
        self._kmax = self.calc_kmax()

    @property
    def kmax(self):
        return self._kmax

    @property
    def influence_factors(self):
        """Returns a dict key and value."""
        names = ["f1", "f2", "f3", "f4", "f5", "I1", "I2"]
        return dict(zip(names, self._influence_factors))

    def calc_c1c2(self) -> Tuple[float, float]:
        """Dimensions are defined in the Mokwa (1999) pg. 269

        :return: Surface surcharge adjust distances to the bottom and top of the foundation.
        :rtype: Tuple()
        """
        c2 = self._z + self._q / self._gamma
        c1 = c2 + self._h
        return (c1, c2)

    def calc_influence_factors(
        self,
    ) -> Tuple[float, float, float, float, float, float, float]:
        """Influence factors equations are given in Mokwa (1999), appendix H, eqn. H.3 to H.7, pg. 380 - 381.
        I1 and I2 are combinations of influence factors required for calculating y1 at the top corners,
        and y2 at the bottom corners.

        :returns Tuple(): A tuple of floats of influence factors (f1, f2, f3, f4, f5, I1, I2)
        """

        c1, c2 = self.calc_c1c2()

        k1 = 2 * c1 / self._b
        k2 = 2 * c2 / self._b

        t1 = k1 - k2
        t2 = k1 + k2
        t3 = np.sqrt(1 + k1**2)
        t4 = np.sqrt(1 + k2**2)
        t5 = np.sqrt(4 + (k1 + k2) ** 2)

        f1 = -t1 * np.log(t1 / (2 + t5)) - 2 * np.log(2 / (t1 + t5))
        f2 = (
            2 * np.log(2 * (k1 + t3) / (t2 + t5))
            + t2 * np.log((2 + t5) / t2)
            - k1**2 * (t5 / t1 - t3 / k1)
        )
        f3 = (
            -2 * k1 * np.log(k1 / (1 + t3))
            + t2 * np.log(t2 / (2 + t5))
            - np.log((t2 + t5) / (2 * (k1 + t3)))
            + t2 / 4 * (t5 - t2)
            - k1 * (t3 - k1)
        )
        if np.abs(k2 - 0) < 1e-4:
            f4 = (
                -2 * np.log(2 * (k2 + t4) / (t2 + t5))
                + t1 * np.log((2 + t5) / t2)
                + k2**2 * (t5 / t2)
            )
        else:
            f4 = (
                -2 * np.log(2 * (k2 + t4) / (t2 + t5))
                + t1 * np.log((2 + t5) / t2)
                + k2**2 * (t5 / t2 - t4 / k2)
            )
        if np.abs(k2 - 0) <= 1e-4:
            f5 = (
                -t2 * np.log(t2 / (2 + t5))
                + np.log((t2 + t5) / (2 * (k2 + t4)))
                - t2 / 4 * (t5 - t2)
                - k2 * (k2 - t4)
            )
        else:
            f5 = (
                2 * k2 * np.log(k2 / (1 + t4))
                - t2 * np.log(t2 / (2 + t5))
                + np.log((t2 + t5) / (2 * (k2 + t4)))
                - t2 / 4 * (t5 - t2)
                - k2 * (k2 - t4)
            )

        I1 = (3 - 4 * self._nu) * f1 + f4 + 4 * (1 - 2 * self._nu) * (1 - self._nu) * f5
        I2 = (3 - 4 * self._nu) * f1 + f2 + 4 * (1 - 2 * self._nu) * (1 - self._nu) * f3

        return (f1, f2, f3, f4, f5, I1, I2)

    def corner_deflections(self, load: float = 1) -> Tuple[float, float]:
        """Deflection at upper (y1) and lower (y2) corners of the horizontally loaded rectangular area

        :param float load: Total horizontal load on the rectangular area
        :returns Tuple(): A tuple of floats of corner deflections.

        """

        _, _, _, _, _, I1, I2 = self._influence_factors

        y1 = (
            load
            / (16 * np.pi * self._modE * self._h)
            * (1 + self._nu)
            / (1 - self._nu)
            * I1
        )
        y2 = (
            load
            / (16 * np.pi * self._modE * self._h)
            * (1 + self._nu)
            / (1 - self._nu)
            * I2
        )

        return (y1, y2)

    def calc_kmax(self, load: float = 1) -> float:
        """Initial elastic stiffness, based on ultimate load and average corner deflections.

        :param float load: applied force
        :returns float: intial elastic stiffness
        """
        # deflections at the top and bottom corner of the loaded area
        y1, y2 = self.corner_deflections(load=load)

        return load / (0.5 * (y1 + y2))
