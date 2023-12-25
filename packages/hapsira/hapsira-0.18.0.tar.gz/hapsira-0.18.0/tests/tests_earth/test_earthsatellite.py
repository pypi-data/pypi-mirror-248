from astropy import units as u
import numpy as np
import pytest

from hapsira.bodies import Earth, Mars
from hapsira.earth import EarthSatellite
from hapsira.earth.enums import EarthGravity
from hapsira.spacecraft import Spacecraft
from hapsira.twobody.orbit import Orbit


def test_earth_satellite_orbit():
    r = [3_539.08827417, 5_310.19903462, 3_066.31301457] * u.km
    v = [-6.49780849, 3.24910291, 1.87521413] * u.km / u.s
    orb = Orbit.from_vectors(Earth, r, v)
    C_D = 2.2 * u.one  # Dimensionless (any value would do)
    A = ((np.pi / 4.0) * (u.m**2)).to(u.km**2)
    m = 100 * u.kg
    spacecraft = Spacecraft(A, C_D, m)
    earth_satellite = EarthSatellite(orb, spacecraft)
    assert isinstance(earth_satellite.orbit, Orbit)


def test_orbit_attractor():
    r = [3_539.08827417, 5_310.19903462, 3_066.31301457] * u.km
    v = [-6.49780849, 3.24910291, 1.87521413] * u.km / u.s
    orb = Orbit.from_vectors(Mars, r, v)
    C_D = 2.2 * u.one  # Dimensionless (any value would do)
    A = ((np.pi / 4.0) * (u.m**2)).to(u.km**2)
    m = 100 * u.kg
    spacecraft = Spacecraft(A, C_D, m)
    with pytest.raises(ValueError) as excinfo:
        EarthSatellite(orb, spacecraft)
    assert "The attractor must be Earth" in excinfo.exconly()


def test_propagate_instance():
    tof = 1.0 * u.min
    orb0 = Orbit.from_classical(
        attractor=Earth,
        a=1000 * u.km,
        ecc=0.75 * u.one,
        inc=63.4 * u.deg,
        raan=0 * u.deg,
        argp=270 * u.deg,
        nu=80 * u.deg,
    )
    C_D = 2.2 * u.one  # Dimensionless (any value would do)
    A = ((np.pi / 4.0) * (u.m**2)).to(u.km**2)
    m = 100 * u.kg
    spacecraft = Spacecraft(A, C_D, m)
    earth_satellite = EarthSatellite(orb0, spacecraft)
    orbit_with_j2 = earth_satellite.propagate(tof=tof, gravity=EarthGravity.J2)
    orbit_without_perturbation = earth_satellite.propagate(tof)
    # orbit_with_atmosphere_and_j2 = earth_satellite.propagate(
    #     tof=tof, gravity=EarthGravity.J2, atmosphere=COESA76()
    # )
    assert isinstance(orbit_with_j2, EarthSatellite)
    # assert isinstance(orbit_with_atmosphere_and_j2, EarthSatellite)
    assert isinstance(orbit_without_perturbation, EarthSatellite)
