class SoilLayer:
    """Class for soil layer, with layer properties."""

    def __init__(
        self,
        c: float,
        phi: float,
        unit_weight: float = 120,
        delta: float = None,
        modE: float = 600000,
        nu: float = 0.5,
        alphac: float = 0.0,
        surcharge: float = 0,
    ) -> None:
        """
        :param c: Mohr-Coulomb c parameter, cohesion.
        :type: float
        :param phi: Mohr-Coulomb phi parameter, friction angle.
        :type: float
        :param unit_weight: Unit weight of the soil.
        :type: float
        :param delta: Friction angle between the soil and the wall/foundation.
        :type: float
        :param modE: Young's modulus of the soil layer.
        :type: float
        :param nu: Poisson's ratio of the soil layer.
        :type: float
        :param alphac: Adhesion coefficient between the soil and the wall/foundation.
        :type: float
        :param surcharge: Surface surcharge above the wall/foundation.
        :type: float
        """
        self._c = c
        self._phi = phi
        self._gamma = unit_weight
        self._delta = 0.4 * self._phi if delta is None else delta
        self._modE = modE
        self._nu = nu
        self._alphac = alphac
        self._q = surcharge

    @property
    def c(self):
        return self._c

    @property
    def phi(self):
        return self._phi

    @property
    def gamma(self):
        return self._gamma

    @property
    def delta(self):
        return self._delta

    @property
    def modE(self):
        return self._modE

    @property
    def nu(self):
        return self._nu

    @property
    def alphac(self):
        return self._alphac

    @property
    def q(self):
        return self._q

    def __repr__(self):
        return f"<SoilLayer(c={self._c:.1f}, phi={self._phi:0.1f}, gamma={self._gamma:0.1f}, modE={self._modE:0.1f}, nu={self._nu:0.2f})>"


class RetainingWall:
    def __init__(
        self,
        height: float,
        width: float = 1,
        depth: float = 0,
        omega: float = 0,
        backfill_surcharge: float = 0,
        backfill_slope: float = 0,
    ) -> None:
        """
        :param height: Height of the wall or the depth between the top and bottom of the foundation
        :type: float
        :param width: Width of the retaining wall or foundation.
        :type: float
        :param depth: The distance to the top of the wall/foundation from the ground surface.
        :type: float
        :param omega: The back face slope of the retaining wall with the vertical. If omega = 0, then the back side of the retaining wall is vertical.
        :type: float
        :param backfill_surcharge: Surface surcharge behind the retaining wall, use consistent units, F/L^2
        :type: float
        :param backfill_slope: The backfill slope behind the wall, degrees. If backfill_slope = 0, then horizontal surface.
        :type: float
        """
        self._h = height
        self._b = width
        self._z = depth
        self._omega = omega
        self._q = backfill_surcharge
        self._beta = backfill_slope

    @property
    def h(self):
        return self._h

    @property
    def b(self):
        return self._b

    @property
    def z(self):
        return self._z

    @property
    def omega(self):
        return self._omega

    @property
    def q(self):
        return self._q

    @property
    def beta(self):
        return self._beta

    def __repr__(self):
        return f"<Foundation(Height={self._h:0.1f}, Width={self._b:0.2f}, Depth={self._z:0.1f})>"
