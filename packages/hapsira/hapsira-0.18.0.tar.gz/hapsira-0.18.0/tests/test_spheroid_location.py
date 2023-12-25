from astropy import units as u
from astropy.tests.helper import assert_quantity_allclose
from hypothesis import given, settings, strategies as st

from hapsira.bodies import Earth
from hapsira.spheroid_location import SpheroidLocation


@st.composite
def with_units(draw, elements, unit):
    lat = draw(elements)
    return lat * unit


def test_cartesian_coordinates():
    expected_cords = [
        3764859.30127275 * u.m,
        2987201.67496698 * u.m,
        4179160.71540021 * u.m,
    ]

    el_cords = (38.43 * u.deg, 41.2 * u.deg, 0 * u.m)

    p = SpheroidLocation(*el_cords, Earth)
    c_cords = p.cartesian_cords

    assert_quantity_allclose(c_cords, expected_cords)


def test_tangential_vectors():
    el_cords = (38.43 * u.deg, 41.2 * u.deg, 0 * u.m)

    p = SpheroidLocation(*el_cords, Earth)

    N = p.N
    v1, v2 = p.tangential_vecs

    assert abs(N @ v1) <= 1e-7
    assert abs(N @ v2) <= 1e-7


def test_visible():
    el_cords = (38.43 * u.deg, 41.2 * u.deg, 0 * u.m)

    p = SpheroidLocation(*el_cords, Earth)

    cords = p.cartesian_cords

    p1 = [cords[i] + 10 * p.N[i] * u.m for i in range(3)]
    p2 = [cords[i] - 10 * p.N[i] * u.m for i in range(3)]

    assert p.is_visible(*p1)
    assert not p.is_visible(*p2)


def test_f():
    expected_f = 0.0033528131

    el_cords = (38.43 * u.deg, 41.2 * u.deg, 0 * u.m)

    p = SpheroidLocation(*el_cords, Earth)

    f = p.f

    assert_quantity_allclose(f, expected_f)


def test_radius_of_curvature():
    expected_roc = 6363141.421601379 * u.m

    el_cords = (38.43 * u.deg, 41.2 * u.deg, 0 * u.m)

    p = SpheroidLocation(*el_cords, Earth)

    roc = p.radius_of_curvature

    assert_quantity_allclose(roc, expected_roc)


def test_distance():
    expected_distance = 6368850.150294118 * u.m
    el_cords = (38.43 * u.deg, 41.2 * u.deg, 0 * u.m)
    point_cords = (10.5 * u.m, 35.5 * u.m, 45.5 * u.m)

    p = SpheroidLocation(*el_cords, Earth)

    distance = p.distance(*point_cords)

    assert_quantity_allclose(distance, expected_distance)


def test_cartesian_conversion_approximate():
    el_cords = (0.7190227 * u.rad, 0.670680 * u.rad, 0 * u.m)

    c_cords = [
        3764258.64785411 * u.m,
        3295359.33856106 * u.m,
        3942945.28570563 * u.m,
    ]

    p = SpheroidLocation(*el_cords, Earth)

    cords = p.cartesian_to_ellipsoidal(*c_cords)

    # TODO: Find ways to improve error margin
    assert_quantity_allclose(el_cords[0], cords[0], 1e-4)
    assert_quantity_allclose(el_cords[1], cords[1], 1e-4)
    assert_quantity_allclose(el_cords[2], cords[2], 1)


@settings(deadline=None)
@given(
    lat=with_units(elements=st.floats(min_value=-1e-2, max_value=1e-2), unit=u.rad),
)
def test_h_calculation_near_lat_singularity(lat):
    body = Earth
    lon = 10 * u.deg
    h = 5 * u.m
    p = SpheroidLocation(lon, lat, h, body)
    cartesian_coords = p.cartesian_cords
    lon_, lat_, h_ = p.cartesian_to_ellipsoidal(*cartesian_coords)

    assert_quantity_allclose(h_, h)
