import pickle

from astropy import units as u
from astropy.tests.helper import assert_quantity_allclose
import pytest

from hapsira.bodies import Body, Earth, Jupiter, Sun
from hapsira.examples import iss


def test_body_has_k_given_in_constructor():
    k = 3.98e5 * u.km**3 / u.s**2
    earth = Body(None, k, "")
    assert earth.k == k


def test_body_from_parameters_raises_valueerror_if_k_units_not_correct():
    wrong_k = 4902.8 * u.kg
    _name = _symbol = ""
    _R = 0
    with pytest.raises(u.UnitsError) as excinfo:
        Body.from_parameters(None, wrong_k, _name, _symbol, _R)
    assert (
        "UnitsError: Argument 'k' to function 'from_parameters' must be in units convertible to 'km3 / s2'."
        in excinfo.exconly()
    )


def test_body_from_parameters_returns_body_object():
    k = 1.26712763e17 * u.m**3 / u.s**2
    R = 71492000 * u.m
    _name = _symbol = "jupiter"
    jupiter = Body.from_parameters(Sun, k, _name, _symbol, Jupiter.R)

    assert jupiter.k == k
    assert jupiter.R == R


def test_body_printing_has_name_and_symbol():
    name = "2 Pallas"
    symbol = "\u26b4"
    k = 1.41e10 * u.m**3 / u.s**2
    pallas2 = Body(None, k, name, symbol)
    assert name in str(pallas2)
    assert symbol in str(pallas2)


def test_earth_has_k_given_in_literature():
    expected_k = 3.986004418e14 * u.m**3 / u.s**2
    k = Earth.k
    assert_quantity_allclose(k.decompose([u.km, u.s]), expected_k)


def test_earth_has_angular_velocity_given_in_literature():
    expected_k = 7.292114e-5 * u.rad / u.s
    k = Earth.angular_velocity
    assert_quantity_allclose(k.decompose([u.rad, u.s]), expected_k)


def test_from_relative():
    TRAPPIST1 = Body.from_relative(
        reference=Sun,
        parent=None,
        k=0.08,  # Relative to the Sun
        name="TRAPPIST",
        symbol=None,
        R=0.114,
    )  # Relative to the Sun

    # Check values properly calculated
    VALUECHECK = Body.from_relative(
        reference=Earth,
        parent=TRAPPIST1,
        k=1,
        name="VALUECHECK",
        symbol=None,
        R=1,
    )
    assert Earth.k == VALUECHECK.k
    assert Earth.R == VALUECHECK.R


def test_attractor_identity_does_not_change_when_pickling(tmp_path):
    d = tmp_path / "tmp"
    d.mkdir()
    f = d / "orbit.pkl"

    with open(f"{f}", "wb") as fh:
        pickle.dump(iss, fh)

    with open(f"{f}", "rb") as fh:
        iss_pickle = pickle.load(fh)

    assert id(iss.attractor) == id(iss_pickle.attractor)
