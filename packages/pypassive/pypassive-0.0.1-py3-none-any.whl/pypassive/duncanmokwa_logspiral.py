import math
from typing import Any
from scipy.optimize import minimize_scalar


class DuncanMokwaLogSpiral:
    """Compute passive pressure on retaining wall.
    ref: Mokwa, R. L. (1999). Investigation of Resistance of Pile Caps to Lateral Loading.
    Duncan, M. J., and Mokwa, R. L. (2001). Passive Earth Pressures: Theories and Tests
    """

    def __init__(self, soil_layer, foundation):
        """Initialize the log spiral method for passive pressure with soil_layer and foundation.

        :param :class: SoilLayer soil_layer:
        :param :class: Foundation foundation:
        """

        self._c: float = soil_layer.c
        self._phi: float = math.radians(soil_layer.phi)
        self._gamma: float = soil_layer.gamma
        self._delta: float = math.radians(soil_layer.delta)
        self._alphac: float = soil_layer.alphac
        self._q: float = soil_layer.q
        self._h: float = foundation.h
        self._alpha: float = math.pi / 4 - self._phi / 2
        self._w: float = 0.0
        self._xo: float = 0.0
        self._yo: float = 0.0
        self._hd: float = 0.0
        self._r: float = 0.0
        self._dist_r: float = 0.0
        self._ro: float = 0.0
        self._theta: float = 0.0
        self._l1: float = 0.0
        self._l2: float = 0.0
        self._l3: float = 0.0
        self._l4: float = 0.0
        self._l5: float = 0.0
        self._mc: float = 0.0
        self._log_spiral_weight: float = 0.0
        self._Eprphi: float = 0.0
        self._Eprc: float = 0.0
        self._Eprq: float = 0.0
        self._Ppphi: float = 0.0
        self._Ppc: float = 0.0
        self._Ppq: float = 0.0
        self._Ep: float = 0.0

    @property
    def w(self) -> float:
        """The width of the log spiral along the surface."""
        return self._w

    @property
    def xo(self) -> float:
        """The horizontal distance of the log spiral center from the wall."""
        return self._xo

    @property
    def yo(self) -> float:
        """The vertical distance of the log spiral center from the top of the wall."""
        return self._yo

    @property
    def alpha(self) -> float:
        """Passive failure angle with the horizontal"""
        return self._alpha

    @property
    def ro(self) -> float:
        """Log spiral initial radius"""
        return self._ro

    @property
    def r(self) -> float:
        """Log spiral radius"""
        return self._r

    @property
    def log_spiral_weight(self) -> float:
        """The weight of the soil in the log spiral region"""
        return self._log_spiral_weight

    @property
    def theta(self) -> float:
        """Angle of the log spiral"""
        return self._theta

    @property
    def hd(self) -> float:
        """The vertical height of the Rankine passive earth pressure region behind the log spiral region."""
        return self._hd

    @property
    def l1(self) -> float:
        """Vertical moment arm of the passive force, Ppphi, from the log spiral center."""
        return self._l1

    @property
    def l2(self) -> float:
        """Moment arm of the log spiral weight from the log spiral center."""
        return self._l2

    @property
    def l3(self) -> float:
        """Moment arm of the Rankine passive force from friction, from passive region behind the log spiral region."""
        return self._l3

    @property
    def l4(self) -> float:
        """Moment arm of the surcharge force from the log spiral center."""
        return self._l4

    @property
    def l5(self) -> float:
        """Moment arm of Rankine passive force from cohesion, from passive region behind the log spiral region."""
        return self._l5

    @property
    def Eprphi(self) -> None:
        """Rankine passive earth pressure due to soil weight and friction angle."""
        return self._Eprphi

    @property
    def Eprc(self) -> None:
        """Rankine passive earth pressure due to cohesion."""
        return self._Eprc

    @property
    def Eprq(self) -> None:
        """Rankine passive earth pressure due to surface surcharge."""
        return self._Eprq

    @property
    def Ep(self) -> float:
        """The ultimate passive pressure."""
        return self._Ep

    @property
    def Ppphi(self) -> float:
        """Passive force component due to soil weight and friction."""
        return self._Ppphi

    @property
    def Ppc(self) -> float:
        """Passive force component due to soil cohesion."""
        return self._Ppc

    @property
    def Ppq(self) -> float:
        """Passive force component due to surface surcharge."""
        return self._Ppq

    def calc_hd1(self, w: float) -> float:
        """Calculate the height of Rankine earth presssure region behind the log spiral region.
        during log spiral radius minimization, Eq. F.3.c

        :param w: length of the failure region on the surface
        :type: float

        :return: hd, the height of the Rankine earth pressure region
        :rtype: float
        """

        return w * math.tan(self._alpha)

    def calc_hd2(self) -> float:
        """Calculate the height of Rankine earth presssure region behind the log spiral region,
        after log spiral radius minimization.
        Eq. F.4.a

        :return: hd, the height of the Rankine earth pressure region
        :rtype: float
        """
        return self._r * math.sin(self._alpha) - self._yo

    def calc_yo(self, xo: float) -> float:
        """Compute ordinate of the log spiral center.
        Eq. F.3.d

        :param xo: abscissa of the log spiral ordinate.float = 5 * self._h
        :type: float

        :return: yo, ordinate of the log spiral center.
        :rtype: float
        """
        return xo * math.tan(self._alpha)

    def calc_log_spiral_ro(self, xo: float) -> float:
        """Compute, ro, the starting radius of the log spiral.
        Eq F.3.e

        :param xo: abscissa of the log spiral center
        :type: float

        :return: ro, initial radius of the log spiral
        :rtype: float
        """

        return math.sqrt((self._h + self._yo) ** 2 + xo**2)

    def calc_log_spiral_theta(self, xo: float) -> float:
        """Compute, log spiral angle theta.
        Eq F.3.f

        :param xo: abscissa of the log spiral center
        :type: float

        :return: theta, log spiral angle
        :rtype: float
        """

        return math.pi / 2 - math.atan(xo / (self._h + self._yo)) - self._alpha

    def calc_log_spiral_r(self) -> float:
        """Compute, log spiral radius at any angle theta from ro.
        Eq F.2

        :return: r, log spiral radius
        :rtype: float
        """

        return self._ro * math.exp(self._theta * math.tan((self._phi)))

    def calc_diagonal_dist(self, w: float, xo: float) -> float:
        """Compute, the diagonal distance from the log spiral center to the end of the log spiral
        Eq F.3.g

        :param w: length of the failure surface on the ground surface
        :type: float
        :param xo: abscissa of the log spiral center
        :type: float

        :return: r, the diagonal distance from the log spiral center to the end of the log spiral
        :rtype: float
        """
        return math.sqrt(w**2 + self._hd**2) + math.copysign(1, xo) * math.sqrt(
            xo**2 + self._yo**2
        )

    def calc_r(self, xo: float, w: float) -> float:
        """Adjust the center of the log spiral such that the diagonal distance and the log spiral
        radius at the end of the log spiral are equal, i.e. minimize abs(log_spiral_r - r)

        :param xo: abscissa of the origin of the log spiral
        :type: float
        :param w: length of the failure surface on the ground surface
        :type: float

        :return: r, the distance from the log spiral center to the end of the log spiral
        :rtype: float
        """

        self._xo = xo

        # step 1: Compute Hd using Eq F.3.c
        self._hd = self.calc_hd1(w)
        # step 3: compute yo using Eqn F.3.d
        self._yo = self.calc_yo(xo)
        # step 4: compute ro using Eqn
        self._ro = self.calc_log_spiral_ro(xo)
        # step 5: compute theta, Eqn. F.3.f
        self._theta = self.calc_log_spiral_theta(xo)
        # step 6: compute using log spiral Eq F.2
        self._r = self.calc_log_spiral_r()
        # step 7: compute r using Eq F.3.g
        self._dist_r = self.calc_diagonal_dist(w, xo)

        return abs(self._r - self._dist_r)

    def calc_l1(self) -> float:
        """Vertical moment arm of the passive force, Ppphi, from the log spiral center, l1.
        F.4.b

        :return: l1, moment arm l1
        :rtype: float
        """
        return 2 / 3 * self._h + self._yo

    def calc_l2(self, w: float) -> float:
        """Moment arm of the log spiral weight from the log spiral center, l2.
        Eqn F.4.d

        :param w: the length of the failure surface on the ground
        :type: float

        :return: moment arm l2
        :rtype: float
        """
        return self._xo + w * (self._h + 2 * self._hd) / (3 * (self._h + self._hd))

    def calc_l3(self) -> float:
        """Moment arm of the Rankine passive force from friction, from passive region behind the log spiral region, l3.
        Eqn F.4.e

        :return: moment arm l3
        :rtype: float
        """
        return 2 / 3 * self._hd + self._yo

    def calc_log_sprial_soil_weight(self, w: float) -> float:
        """Compute the weight of the log spiral region
        Eqn F.5

        :param w: lenght of the failure surface on the ground
        :type: float

        :return: the weight of the log spiral
        :rtype: float
        """
        return self._gamma * (
            (self._r**2 - self._ro**2) / (4 * math.tan(self._phi))
            - 1 / 2 * self._xo * self._h
            + 1 / 2 * w * self._hd
        )

    def calc_Eprphi(self) -> float:
        """Rankine earth pressure due to soil weight,
        Eqn F.6

        :return: Rankine earth pressure due to friction and soil weight
        :rtype: float
        """
        return (1 / 2 * self._gamma * self._hd**2) * (
            math.tan(math.pi / 4 + self._phi / 2) ** 2
        )

    def calc_l4(self, w: float) -> float:
        """Moment arm of the surcharge force from the log spiral center, l4.
        Eq F.8

        :param w: the length of the failure surface on the ground
        :type: float

        :return: moment arm l4
        :rtype: float
        """
        return self._xo + w / 2

    def calc_l5(self) -> float:
        """Moment arm of Rankine passive force from cohesion, from passive region behind the log spiral region.
        Eq F.9

        :return: moment arm l5
        :rtype: float
        """
        return self._yo + self._hd / 2

    def calc_Eprc(self) -> float:
        """Rankine earth pressure due to cohesion acting on the vertical face in the Rankine region
        Eqn F.10

        :return: Rankine earth pressure due to cohesion acting on the vertical face in the Rankine region
        :rtype: float
        """
        return 2 * self._c * math.tan(math.pi / 4 + self._phi / 2) * self._hd

    def calc_Mc(self) -> float:
        """Moment due to cohesion about point O
        Eqn. F.11

        :return: moment due to cohesion
        :rtype: float
        """
        return self._c / (2 * math.tan(self._phi)) * (self._r**2 - self._ro**2)

    def calc_Eprq(self) -> float:
        """Rankine earth pressure due to surcharge in the Rankine region
        F.13

        :return: Rankine earth pressure due to surcharge
        :rtype: float
        """
        return self._q * math.tan(math.pi / 4 + self._phi / 2) ** 2 * self._hd

    def calc_moment_arms(self, w: float) -> None:
        """Compute remaining quantities and moment arms after determing log spiral radius from minimization"""
        self._hd = self.calc_hd2()
        self._l1 = self.calc_l1()
        self._l2 = self.calc_l2(w)
        self._l3 = self.calc_l3()
        self._l4 = self.calc_l4(w)
        self._l5 = self.calc_l5()
        self._log_spiral_weight = self.calc_log_sprial_soil_weight(w)

    def calc_Rankine_passive_earth_pressures(self) -> None:
        """Compute Rankine passive earth pressures"""
        self._Eprphi = self.calc_Eprphi()
        self._Eprc = self.calc_Eprc()
        self._Eprq = self.calc_Eprq()

    def calc_Ppphi(self) -> float:
        """Earth pressure due to self weight of the soil and friction angle
        Eqn F.7

        :return: Passive force from self weight and friction angle
        :rtype: float
        """

        return (self._l2 * self._log_spiral_weight + self._l3 * self._Eprphi) / (
            self._l1 * math.cos(self._delta) - self._xo * math.sin(self._delta)
        )

    def calc_Ppc(self) -> float:
        """Earth pressure due to cohesion,
        Eq F.12

        :return: Earth pressure due to cohesion
        :rtype: float
        """

        self._mc = self.calc_Mc()

        return (
            self._mc
            + self._l5 * self._Eprc
            + self._alphac * self._c * self._h * self._xo
        ) / (self._l1 * math.cos(self._delta) - self._xo * math.sin(self._delta))

    def calc_Ppq(self, w: float) -> float:
        """Passvive force at the wall face due to surface surcharge
        Eqn F.14

        :return: Passive force due to surface surcharge
        :rtype: float

        """

        return (self._l4 * w * self._q + self._l5 * self._Eprq) / (
            self._l1 * math.cos(self._delta) - self._xo * math.sin(self._delta)
        )

    def calc_Ep(self, w: float) -> float:
        """Ultimate passive earth pressure
        Eqn F.1

        :param w: the length of the failure surface on the ground
        :type: float

        """
        # minimization to compute the extent of the log spiral curve
        res = minimize_scalar(
            self.calc_r,
            args=(w),
            bounds=(-5.0 * self._h, 5 * self._h),
            method="bounded",
        )

        self._xo = res.x
        self.calc_moment_arms(w)
        self.calc_Rankine_passive_earth_pressures()
        self._Ppphi = self.calc_Ppphi()
        self._Ppc = self.calc_Ppc()
        self._Ppq = self.calc_Ppq(w)

        return self._Ppphi + self._Ppc + self._Ppq

    def passive_force(self) -> Any:
        # minimize ultimate passive earth pressure by changing the horizontal extent of the log spiral
        bnds = (0.25 * self._h, 5 * self._h)
        res = minimize_scalar(
            self.calc_Ep,
            bounds=bnds,
            method="bounded",
        )
        self._w = res.x
        self._Ep = res.fun

        return res
