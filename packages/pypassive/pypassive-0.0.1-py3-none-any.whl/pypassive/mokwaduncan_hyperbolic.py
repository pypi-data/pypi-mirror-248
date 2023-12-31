import numpy as np
from typing import Any


class MokwaDuncanHyperbolic:
    """Influence factors for computing the deflection of horizontally loaded vertical rectangle.
    ref: Mokwa, R. L. (1999). Investigation of the Resistance of Pile Caps to Lateral Loading.

    Use consistent units for calculations and adjust the units in postprocessing the results.
    """

    def __init__(
        self, pult: float = 0, kmax: float = 1, delta_max: float = 1, rf: float = None
    ) -> None:
        """
        :param float pult: Ultimate load
        :param float kmax: Initial tangent stiffness
        :param float delta_max: Maximum displacement at ultimate load
        :param float rf: Failure ratio, by default the value is None, if a value is supplied then
        the given value of rf is used, if rf = None then rf is computed.
        """
        self._pult = pult
        self._kmax = kmax
        self._delta_max = delta_max
        self._rf = self.calc_rf() if rf == None else rf

    def calc_rf(self) -> float:
        """Failure ratio as defined in Duncan and Change (1970). The ratio of the asymptotic
         stress of the hyperbolic curve to the soil strength.

        :returns float: Failure ratio
        """

        return (self._delta_max / self._pult - 1 / self._kmax) * (
            self._pult / self._delta_max
        )

    def hyperbolic_force_displacement(self, ys: Any = []) -> Any:
        """Hyperbolic force-displacement curve.

        :param Any ys: horizontal displacements
        :param float pult: Failure load
        :param Any dmax_height_ratio: Ratio of the assumed displacement at failure to the height of the rectangular area (footing depth, retaining wall height).
        """
        if len(ys) == 0:
            ys = np.logspace(-3.1, self._delta_max)

        return (ys, ys / ((1 / self._kmax + ys * self._rf / self._pult)))
