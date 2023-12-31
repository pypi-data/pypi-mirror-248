import math
from typing import Any
from scipy.optimize import minimize_scalar


class AlqarawiLogSpiral:
    """Compute passive pressure on retaining wall.
    ref: Alqarawi, A. S., Leo, C. J., Liyanapathirana, D. S., Sigdel, L., Lu, M., and Hu, P. (2012).
    A spreadsheet-based technique to calculate the passive soil pressure based on log-spiral method.
    Computers and Geotechnics 130.
    """

    def __init__(self, soil_layer, retaining_wall):
        """Initialize the log spiral method for passive pressure with soil_layer and foundation.

        :param soil_layer: a class defined with soil layer properties
        :type: :class:SoilLayer
        :param retaining_wall: a class defined with retaining wall dimensions and surcharge loading.
        :type: :class:RetainingWall
        """

        self._c: float = soil_layer.c
        self._phi: float = math.radians(soil_layer.phi)
        self._gamma: float = soil_layer.gamma
        self._delta: float = math.radians(soil_layer.delta)
        self._h: float = retaining_wall.h
        self._omega: float = math.radians(retaining_wall.omega)
        self._beta: float = math.radians(retaining_wall.beta)
        self._q: float = retaining_wall.q
        # Eqn 6, Wall height is the vertical projection so no need for Eqn 5
        # |ab| = H/cos(omega)
        self._ab = retaining_wall.h / math.cos(self._omega)
        # Eqn 7
        self._xhat: float = retaining_wall.h * math.tan(self._omega)
        # Eqn 1
        self._alpha1: float = self.calc_alpha1()
        # Eqn 2
        self._alpha2: float = self.calc_alpha2()
        # Eqn 7
        self._eta: float = self._alpha1 - self._beta
        # Eqn 31
        self._nu: float = self._eta - self._delta + self._omega
        # rest of the coordinates and lengths/distances
        self._xa: float = 0
        self._ya: float = 0
        self._xb: float = 0
        self._yb: float = 0
        self._xg: float = 0
        self._yg: float = 0
        self._rg: float = 0
        self._xf: float = 0
        self._yf: float = 0
        self._ag: float = 0
        self._fg: float = 0
        # Moments
        self._Mrw: float = 0
        self._Mqh: float = 0
        self._Mobg: float = 0
        self._Moba: float = 0
        self._Mabg: float = 0
        self._Mq: float = 0
        self._Magfp: float = 0
        self._l1: float = 0
        # passive ford
        self._Pp: float = 0

    def calc_alpha1(self) -> float:
        """Eq 1"""
        return (
            math.pi / 4
            - self._phi / 2
            + 0.5 * math.asin(math.sin(self._beta) / math.sin(self._phi))
            - self._beta / 2
        )

    def calc_alpha2(self) -> float:
        """Eq 2"""
        return (
            math.pi / 4
            - self._phi / 2
            - 0.5 * math.asin(math.sin(self._beta) / math.sin(self._phi))
            + self._beta / 2
        )

    def calc_coords(self, zeta: float) -> None:
        """Coordinates that define salient points"""
        # Eqn 9
        self._xa = abs(zeta) * math.cos(self._eta)
        # Eqn 10
        self._ya = abs(zeta) * math.sin(self._eta)
        # Eqn 11
        self._ro = math.sqrt((self._h + self._ya) ** 2 + (self._xa + self._xhat) ** 2)
        # Eqn 12
        self._xb = self._xa + abs(self._xhat)
        # Eqn 13
        self._yb = self._ya + self._h
        # Eqn 14
        self._thetag = math.asin(self._yb / self._ro) - self._eta
        # Eqn 3
        self._rg = self._ro * math.exp(self._thetag * math.tan(self._phi))
        # Eqn 15
        self._xg = self._rg * math.cos(self._eta)
        # Eqn 16
        self._yg = self._rg * math.sin(self._eta)
        # Eqn 17
        self._ag = self._rg - abs(zeta)
        # Eqn 18
        self._fg = self._ag * math.sin(self._alpha1)
        # Eqn 19
        self._xf = self._xg - self._fg * math.sin(self._beta)
        # Eqn 20
        self._yf = self._yg - self._fg * math.cos(self._beta)
        # angle between the ro and the vertical
        self._lambda = math.atan(self._xb / self._yb)

    def calc_Mobg(self) -> float:
        # Eqn 27
        t1 = (
            (self._ro**3 * math.cos(self._lambda))
            / (3 * (1 + 9 * math.tan(self._phi) ** 2))
            * (
                1
                + math.exp(3 * self._thetag * math.tan(self._phi))
                * (
                    3 * math.tan(self._phi) * math.sin(self._thetag)
                    - math.cos(self._thetag)
                )
            )
        )
        t2 = (
            (self._ro**3 * math.sin(self._lambda))
            / (3 * (1 + 9 * math.tan(self._phi) ** 2))
            * (
                math.exp(3 * self._thetag * math.tan(self._phi))
                * (
                    math.sin(self._thetag)
                    + 3 * math.tan(self._phi) * math.cos(self._thetag)
                )
                - 3 * math.tan(self._phi)
            )
        )
        return t1 + t2

    def calc_Moba(self) -> float:
        # Eqn 29
        return (
            1 / 6 * (self._xa * self._yb - self._xb * self._ya) * (self._xa + self._xb)
        )

    def calc_Mabg(self) -> float:
        # Eqn 30
        self._Mobg = self.calc_Mobg()
        self._Moba = self.calc_Moba()
        return (self._Mobg - self._Moba) * self._gamma

    def calc_l1(self, zeta: float) -> float:
        # Eq 32, 33, and 34
        return abs(zeta) * math.sin(self._nu) + 2 / 3 * self._ab * math.cos(self._delta)

    def calc_afp(self) -> None:
        # Eqn 38
        af = abs(self._xf - self._xa) / math.cos(self._beta)
        # Eqn 37
        return af + self._fg * math.tan(self._beta)

    def calc_Mq(self) -> float:
        # Eqn 38
        afp = self.calc_afp()
        # Eqn 36
        surcharge_load = self._q * afp
        return surcharge_load * (self._xa + (self._xg - self._xa) / 2)

    def calc_Mrw(self) -> float:
        kp = self.calc_kp()
        # Eqn 41
        hrw = self._fg / math.cos(self._beta)
        # Eqn 35
        lrw = self._rg * math.sin(self._alpha1) - 1 / 3 * self._fg
        prw = 1 / 2 * kp * self._gamma * hrw**2 * math.cos(self._beta)
        return prw * lrw

    def calc_Mqh(self) -> float:
        # Eqn 41
        hrw = self._fg / math.cos(self._beta)
        # Eqn 42
        kp = self.calc_kp()
        fq = self._q * math.cos(self._beta) * kp * hrw
        lq = self._rg * math.sin(self._alpha1) - self._fg / 2
        return fq * lq

    def calc_Magfp(self):
        afp = self.calc_afp()
        # Eq 43
        return 1 / 6 * afp * self._fg * self._gamma * (self._xa + self._xg + self._xg)

    def calc_kp(self) -> float:
        """Rankine's passive pressure coefficient for sloped backfill."""
        # Eqn 42
        return (
            math.cos(self._beta)
            + math.sqrt(math.cos(self._beta) ** 2 - math.cos(self._phi) ** 2)
        ) / (
            math.cos(self._beta)
            - math.sqrt(math.cos(self._beta) ** 2 - math.cos(self._phi) ** 2)
        )

    def calc_moments(self) -> None:
        self._Mabg = self.calc_Mabg()
        self._Mq = self.calc_Mq()
        self._Mqh = self.calc_Mqh()
        self._Mrw = self.calc_Mrw()
        self._Magfp = self.calc_Magfp()

    def calc_passive_force_all(self, zeta: float) -> float:
        """Determine the total passive force from moment equilibrium."""
        self.calc_coords(zeta)
        self.calc_moments()
        self._l1 = self.calc_l1(zeta)

        return 1 / self._l1 * (self._Mrw + self._Mqh + self._Mabg + self._Mq + self._Magfp)

    def passive_force(self) -> float:
        """Minize the passive force by changing, zeta, the center of the log spiral"""
        bnds = (-3.0 * self._h, 0 * self._h)
        res = minimize_scalar(
            self.calc_passive_force_all,
            bounds=bnds,
            method="bounded",
        )
        self._zeta = res.x
        self._Ep = res.fun

        return res
