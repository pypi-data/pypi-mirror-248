from astropy import time, units as u
from astropy.coordinates import CartesianRepresentation
from astropy.tests.helper import assert_quantity_allclose
from hypothesis import given, settings, strategies as st
import numpy as np
from numpy.testing import assert_allclose
import pytest
from pytest import approx

from hapsira.bodies import Earth, Moon, Sun
from hapsira.constants import J2000
from hapsira.core.elements import rv2coe
from hapsira.core.propagation import func_twobody
from hapsira.examples import iss
from hapsira.frames import Planes
from hapsira.twobody import Orbit
from hapsira.twobody.propagation import (
    ALL_PROPAGATORS,
    ELLIPTIC_PROPAGATORS,
    HYPERBOLIC_PROPAGATORS,
    PARABOLIC_PROPAGATORS,
    CowellPropagator,
    DanbyPropagator,
    FarnocchiaPropagator,
    GoodingPropagator,
    MarkleyPropagator,
    RecseriesPropagator,
    ValladoPropagator,
)
from hapsira.util import norm


@pytest.fixture(scope="module")
def halley():
    return Orbit.from_vectors(
        Sun,
        [-9018878.63569932, -94116054.79839276, 22619058.69943215] * u.km,
        [-49.95092305, -12.94843055, -4.29251577] * u.km / u.s,
    )


@pytest.mark.parametrize("ecc", [0.9, 0.99, 0.999, 0.9999, 0.99999])
@pytest.mark.parametrize("propagator", ELLIPTIC_PROPAGATORS)
def test_elliptic_near_parabolic(ecc, propagator):
    rtol = 1e-7
    if propagator in (RecseriesPropagator, ValladoPropagator):
        rtol = 1e-6
    if propagator is ValladoPropagator and ecc >= 0.99999:
        rtol = 1e-5

    _a = 0.0 * u.rad
    tof = 1.0 * u.min
    ss0 = Orbit.from_classical(
        attractor=Earth,
        a=10000 * u.km,
        ecc=ecc * u.one,
        inc=_a,
        raan=_a,
        argp=_a,
        nu=1.0 * u.rad,
    )

    orb_cowell = ss0.propagate(tof, method=CowellPropagator())
    orb_propagator = ss0.propagate(tof, method=propagator())

    assert_quantity_allclose(orb_propagator.r, orb_cowell.r, rtol=rtol)
    assert_quantity_allclose(orb_propagator.v, orb_cowell.v, rtol=rtol)


@pytest.mark.parametrize("ecc", [1.0001, 1.001, 1.01, 1.1])
@pytest.mark.parametrize("propagator", HYPERBOLIC_PROPAGATORS)
def test_hyperbolic_near_parabolic(ecc, propagator):
    _a = 0.0 * u.rad
    tof = 1.0 * u.min
    ss0 = Orbit.from_classical(
        attractor=Earth,
        a=-10000 * u.km,
        ecc=ecc * u.one,
        inc=_a,
        raan=_a,
        argp=_a,
        nu=1.0 * u.rad,
    )

    orb_cowell = ss0.propagate(tof, method=CowellPropagator())
    orb_propagator = ss0.propagate(tof, method=propagator())

    assert_quantity_allclose(orb_propagator.r, orb_cowell.r)
    assert_quantity_allclose(orb_propagator.v, orb_cowell.v)


@pytest.mark.parametrize("method", [MarkleyPropagator()])
def test_near_equatorial(method):
    # TODO: Extend to other propagators?
    r = [8.0e3, 1.0e3, 0.0] * u.km
    v = [-0.5, -0.5, 0.0001] * u.km / u.s
    tof = 1.0 * u.h
    ss0 = Orbit.from_vectors(Earth, r, v)

    orb_cowell = ss0.propagate(tof, method=CowellPropagator())
    orb_propagator = ss0.propagate(tof, method=method)

    assert_quantity_allclose(orb_propagator.r, orb_cowell.r, rtol=1e-4)
    assert_quantity_allclose(orb_propagator.v, orb_cowell.v, rtol=1e-4)


@pytest.mark.parametrize("propagator", ALL_PROPAGATORS)
def test_propagation(propagator):
    # Data from Vallado, example 2.4
    r0 = [1131.340, -2282.343, 6672.423] * u.km
    v0 = [-5.64305, 4.30333, 2.42879] * u.km / u.s
    expected_r = [-4219.7527, 4363.0292, -3958.7666] * u.km
    expected_v = [3.689866, -1.916735, -6.112511] * u.km / u.s

    ss0 = Orbit.from_vectors(Earth, r0, v0)
    tof = 40 * u.min
    ss1 = ss0.propagate(tof, method=propagator())

    r, v = ss1.rv()

    assert_quantity_allclose(r, expected_r, rtol=1e-5)
    assert_quantity_allclose(v, expected_v, rtol=1e-4)


def test_propagating_to_certain_nu_is_correct():
    # Take an elliptic orbit
    a = 1.0 * u.AU
    ecc = 1.0 / 3.0 * u.one
    _a = 0.0 * u.rad
    nu = 10 * u.deg
    elliptic = Orbit.from_classical(
        attractor=Sun, a=a, ecc=ecc, inc=_a, raan=_a, argp=_a, nu=nu
    )

    elliptic_at_perihelion = elliptic.propagate_to_anomaly(0.0 * u.rad)
    r_per, _ = elliptic_at_perihelion.rv()

    elliptic_at_aphelion = elliptic.propagate_to_anomaly(np.pi * u.rad)
    r_ap, _ = elliptic_at_aphelion.rv()

    assert_quantity_allclose(norm(r_per), a * (1.0 - ecc))
    assert_quantity_allclose(norm(r_ap), a * (1.0 + ecc))

    # TODO: Test specific values
    assert elliptic_at_perihelion.epoch > elliptic.epoch
    assert elliptic_at_aphelion.epoch > elliptic.epoch

    # Test 10 random true anomaly values
    # TODO: Rework this test
    for nu in np.random.uniform(low=-np.pi, high=np.pi, size=10):
        elliptic = elliptic.propagate_to_anomaly(nu * u.rad)
        r, _ = elliptic.rv()
        assert_quantity_allclose(norm(r), a * (1.0 - ecc**2) / (1 + ecc * np.cos(nu)))


def test_propagate_to_anomaly_in_the_past_fails_for_open_orbits():
    r0 = [Earth.R.to(u.km).value + 300, 0, 0] * u.km
    v0 = [0, 15, 0] * u.km / u.s
    orb = Orbit.from_vectors(Earth, r0, v0)

    with pytest.raises(ValueError, match="True anomaly -0.02 rad not reachable"):
        orb.propagate_to_anomaly(orb.nu - 1 * u.deg)


def test_propagate_accepts_timedelta():
    # Data from Vallado, example 2.4
    r0 = [1131.340, -2282.343, 6672.423] * u.km
    v0 = [-5.64305, 4.30333, 2.42879] * u.km / u.s
    expected_r = [-4219.7527, 4363.0292, -3958.7666] * u.km
    expected_v = [3.689866, -1.916735, -6.112511] * u.km / u.s

    ss0 = Orbit.from_vectors(Earth, r0, v0)
    tof = time.TimeDelta(40 * u.min)
    ss1 = ss0.propagate(tof)

    r, v = ss1.rv()

    assert_quantity_allclose(r, expected_r, rtol=1e-5)
    assert_quantity_allclose(v, expected_v, rtol=1e-4)


def test_propagation_hyperbolic():
    # Data from Curtis, example 3.5
    r0 = [Earth.R.to(u.km).value + 300, 0, 0] * u.km
    v0 = [0, 15, 0] * u.km / u.s
    expected_r_norm = 163180 * u.km
    expected_v_norm = 10.51 * u.km / u.s

    ss0 = Orbit.from_vectors(Earth, r0, v0)
    tof = 14941 * u.s
    ss1 = ss0.propagate(tof)
    r, v = ss1.rv()

    assert_quantity_allclose(norm(r), expected_r_norm, rtol=1e-4)
    assert_quantity_allclose(norm(v), expected_v_norm, rtol=1e-3)


@pytest.mark.parametrize("propagator", PARABOLIC_PROPAGATORS)
def test_propagation_parabolic(propagator):
    # Example from Howard Curtis (3rd edition), section 3.5, problem 3.15
    p = 2.0 * 6600 * u.km
    _a = 0.0 * u.deg
    orbit = Orbit.parabolic(Earth, p, _a, _a, _a, _a)
    orbit = orbit.propagate(0.8897 / 2.0 * u.h, method=propagator())

    _, _, _, _, _, nu0 = rv2coe(
        Earth.k.to(u.km**3 / u.s**2).value,
        orbit.r.to(u.km).value,
        orbit.v.to(u.km / u.s).value,
    )
    assert_quantity_allclose(nu0, np.deg2rad(90.0), rtol=1e-4)

    orbit = Orbit.parabolic(Earth, p, _a, _a, _a, _a)
    orbit = orbit.propagate(36.0 * u.h, method=propagator())
    assert_quantity_allclose(norm(orbit.r), 304700.0 * u.km, rtol=1e-4)


def test_propagation_zero_time_returns_same_state():
    # Bug #50
    r0 = [1131.340, -2282.343, 6672.423] * u.km  # type: u.Quantity
    v0 = [-5.64305, 4.30333, 2.42879] * u.km / u.s
    ss0 = Orbit.from_vectors(Earth, r0, v0)
    tof = 0 * u.s

    ss1 = ss0.propagate(tof)

    r, v = ss1.rv()

    assert_quantity_allclose(r, r0)
    assert_quantity_allclose(v, v0)


def test_propagation_hyperbolic_zero_time_returns_same_state():
    ss0 = Orbit.from_classical(
        attractor=Earth,
        a=-27112.5464 * u.km,
        ecc=1.25 * u.one,
        inc=0 * u.deg,
        raan=0 * u.deg,
        argp=0 * u.deg,
        nu=0 * u.deg,
    )
    r0, v0 = ss0.rv()
    tof = 0 * u.s

    ss1 = ss0.propagate(tof)

    r, v = ss1.rv()

    assert_quantity_allclose(r, r0, atol=1e-24 * u.km)
    assert_quantity_allclose(v, v0, atol=1e-27 * u.km / u.s)


def test_apply_zero_maneuver_returns_equal_state():
    _d = 1.0 * u.AU  # Unused distance
    _ = 0.5 * u.one  # Unused dimensionless value
    _a = 1.0 * u.deg  # Unused angle
    ss = Orbit.from_classical(
        attractor=Sun, a=_d, ecc=_, inc=_a, raan=_a, argp=_a, nu=_a
    )
    dt = 0 * u.s
    dv = [0, 0, 0] * u.km / u.s
    orbit_new = ss.apply_maneuver([(dt, dv)])
    assert_allclose(orbit_new.r.to(u.km).value, ss.r.to(u.km).value)
    assert_allclose(orbit_new.v.to(u.km / u.s).value, ss.v.to(u.km / u.s).value)


def test_cowell_propagation_with_zero_acceleration_equals_kepler():
    # Data from Vallado, example 2.4

    r0 = np.array([1131.340, -2282.343, 6672.423]) * u.km
    v0 = np.array([-5.64305, 4.30333, 2.42879]) * u.km / u.s
    tofs = [40 * 60.0] * u.s

    orbit = Orbit.from_vectors(Earth, r0, v0)

    expected_r = np.array([-4219.7527, 4363.0292, -3958.7666]) * u.km
    expected_v = np.array([3.689866, -1.916735, -6.112511]) * u.km / u.s

    method = CowellPropagator()
    rrs, vvs = method.propagate_many(orbit._state, tofs)

    assert_quantity_allclose(rrs[0], expected_r, rtol=1e-5)
    assert_quantity_allclose(vvs[0], expected_v, rtol=1e-4)


def test_cowell_propagation_circle_to_circle():
    # From [Edelbaum, 1961]
    accel = 1e-7

    def constant_accel(t0, u_, k):
        v = u_[3:]
        norm_v = (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** 0.5
        return accel * v / norm_v

    def f(t0, u_, k):
        du_kep = func_twobody(t0, u_, k)
        ax, ay, az = constant_accel(t0, u_, k)
        du_ad = np.array([0, 0, 0, ax, ay, az])

        return du_kep + du_ad

    ss = Orbit.circular(Earth, 500 * u.km)
    tofs = [20] * ss.period

    method = CowellPropagator(f=f)
    rrs, vvs = method.propagate_many(ss._state, tofs)

    orb_final = Orbit.from_vectors(Earth, rrs[0], vvs[0])

    da_a0 = (orb_final.a - ss.a) / ss.a
    dv_v0 = abs(norm(orb_final.v) - norm(ss.v)) / norm(ss.v)
    assert_quantity_allclose(da_a0, 2 * dv_v0, rtol=1e-2)

    dv = abs(norm(orb_final.v) - norm(ss.v))
    accel_dt = accel * u.km / u.s**2 * tofs[0]
    assert_quantity_allclose(dv, accel_dt, rtol=1e-2)


def test_propagate_to_date_has_proper_epoch():
    # Data from Vallado, example 2.4
    r0 = [1131.340, -2282.343, 6672.423] * u.km
    v0 = [-5.64305, 4.30333, 2.42879] * u.km / u.s
    init_epoch = J2000
    final_epoch = time.Time("2000-01-01 12:40:00", scale="tdb")

    expected_r = [-4219.7527, 4363.0292, -3958.7666] * u.km
    expected_v = [3.689866, -1.916735, -6.112511] * u.km / u.s

    ss0 = Orbit.from_vectors(Earth, r0, v0, epoch=init_epoch)
    ss1 = ss0.propagate(final_epoch)

    r, v = ss1.rv()

    assert_quantity_allclose(r, expected_r, rtol=1e-5)
    assert_quantity_allclose(v, expected_v, rtol=1e-4)

    # Tolerance should be higher, see https://github.com/astropy/astropy/issues/6638
    assert (ss1.epoch - final_epoch).sec == approx(0.0, abs=1e-6)


@pytest.mark.filterwarnings("ignore::erfa.core.ErfaWarning")
@pytest.mark.parametrize(
    "method", [DanbyPropagator(), MarkleyPropagator(), GoodingPropagator()]
)
def test_propagate_long_times_keeps_geometry(method):
    # TODO: Extend to other propagators?
    # See https://github.com/hapsira/hapsira/issues/265
    time_of_flight = 100 * u.year

    res = iss.propagate(time_of_flight, method=method)

    assert_quantity_allclose(iss.a, res.a)
    assert_quantity_allclose(iss.ecc, res.ecc)
    assert_quantity_allclose(iss.inc, res.inc)
    assert_quantity_allclose(iss.raan, res.raan)
    assert_quantity_allclose(iss.argp, res.argp)

    assert_quantity_allclose(
        (res.epoch - iss.epoch).to(time_of_flight.unit), time_of_flight
    )


@pytest.mark.filterwarnings("ignore::erfa.core.ErfaWarning")
def test_long_propagations_vallado_agrees_farnocchia():
    tof = 100 * u.year
    r_mm, v_mm = iss.propagate(tof, method=FarnocchiaPropagator()).rv()
    r_k, v_k = iss.propagate(tof, method=ValladoPropagator()).rv()
    assert_quantity_allclose(r_mm, r_k)
    assert_quantity_allclose(v_mm, v_k)

    r_halleys = [
        -9018878.63569932,
        -94116054.79839276,
        22619058.69943215,
    ]  # km
    v_halleys = [-49.95092305, -12.94843055, -4.29251577]  # km/s
    halleys = Orbit.from_vectors(Sun, r_halleys * u.km, v_halleys * u.km / u.s)

    r_mm, v_mm = halleys.propagate(tof, method=FarnocchiaPropagator()).rv()
    r_k, v_k = halleys.propagate(tof, method=ValladoPropagator()).rv()
    assert_quantity_allclose(r_mm, r_k)
    assert_quantity_allclose(v_mm, v_k)


def test_farnocchia_propagation_very_high_ecc_does_not_fail():
    # Regression test for #1296.
    r = np.array([-500, 1500, 4012.09]) << u.km
    v = np.array([5021.38, -2900.7, 1000.354]) << u.km / u.s
    orbit = Orbit.from_vectors(Earth, r, v, epoch=time.Time("2020-01-01"))

    tofs = [74] << u.s  # tof = 74s and above is the critical region
    method = FarnocchiaPropagator()
    coords, _ = method.propagate_many(orbit._state, tofs)

    assert not np.isnan(coords).any()


@st.composite
def with_units(draw, elements, unit):
    value = draw(elements)
    return value * unit


@settings(deadline=None)
@given(
    tof=with_units(
        elements=st.floats(
            min_value=80, max_value=120, allow_nan=False, allow_infinity=False
        ),
        unit=u.year,
    )
)
@pytest.mark.parametrize("method", [FarnocchiaPropagator(), ValladoPropagator()])
def test_long_propagation_preserves_orbit_elements(tof, method, halley):
    expected_slow_classical = halley.classical()[:-1]

    slow_classical = halley.propagate(tof, method=method).classical()[:-1]

    for element, expected_element in zip(slow_classical, expected_slow_classical):
        assert_quantity_allclose(element, expected_element)


def test_propagation_sets_proper_epoch():
    expected_epoch = time.Time("2017-09-01 12:05:50", scale="tdb")

    r = [-2.76132873e08, -1.71570015e08, -1.09377634e08] * u.km
    v = [13.17478674, -9.82584125, -1.48126639] * u.km / u.s
    florence = Orbit.from_vectors(Sun, r, v, plane=Planes.EARTH_ECLIPTIC)

    propagated = florence.propagate(expected_epoch)

    assert propagated.epoch == expected_epoch


def test_sample_around_moon_works():
    # See https://github.com/hapsira/hapsira/issues/649
    orbit = Orbit.circular(Moon, 100 << u.km)

    coords = orbit.sample(10)

    assert isinstance(coords, CartesianRepresentation)
    assert len(coords) == 10


def test_propagate_around_moon_works():
    # See https://github.com/hapsira/hapsira/issues/649
    orbit = Orbit.circular(Moon, 100 << u.km)
    new_orbit = orbit.propagate(1 << u.h)

    assert_quantity_allclose((new_orbit.epoch - orbit.epoch).to(u.h), 1 << u.h)


@pytest.mark.parametrize("propagator", ALL_PROPAGATORS)
def test_propagator_with_zero_eccentricity(propagator):
    attractor = Earth
    altitude = 300 * u.km
    orbit = Orbit.circular(attractor, altitude)
    time_of_flight = 50 * u.s
    res = orbit.propagate(time_of_flight, method=propagator())

    assert_quantity_allclose(orbit.a, res.a)
    assert_quantity_allclose(orbit.ecc, res.ecc, atol=1e-15)
    assert_quantity_allclose(orbit.inc, res.inc)
    assert_quantity_allclose(orbit.raan, res.raan)
    assert_quantity_allclose(orbit.argp, res.argp)
