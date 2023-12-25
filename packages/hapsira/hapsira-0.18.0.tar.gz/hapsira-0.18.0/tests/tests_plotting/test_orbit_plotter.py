import sys

from astropy import time, units as u
from astropy.coordinates import CartesianDifferential, CartesianRepresentation
from astropy.time import Time
from matplotlib import pyplot as plt
import pytest

from hapsira.bodies import Earth, Jupiter, Mars, Sun
from hapsira.constants import J2000_TDB
from hapsira.ephem import Ephem
from hapsira.examples import churi, iss, molniya
from hapsira.frames import Planes
from hapsira.maneuver import Maneuver
from hapsira.plotting import OrbitPlotter
from hapsira.plotting.orbit.backends import (
    DEFAULT_ORBIT_PLOTTER_BACKENDS,
    DEFAULT_ORBIT_PLOTTER_BACKENDS_2D,
    DEFAULT_ORBIT_PLOTTER_BACKENDS_3D,
    Matplotlib2D,
)
from hapsira.twobody import Orbit
from hapsira.util import time_range

# @pytest.mark.parametrize("backend", SUPPORTED_ORBIT_PLOTTER_BACKENDS)
# def test_get_figure_has_expected_properties(backend):
#     plotter = OrbitPlotter(backend=backend_name)
#     scene = plotter.show()
#
#     assert scene.data == ()
#     assert scene.layout.autosize is True
#     assert "xaxis" in scene.layout
#     assert "yaxis" in scene.layout


# def test_plotter_with_plotly3D_backend_has_expected_properties():
#     frame = OrbitPlotter()
#     figure = frame.show()
#
#     assert figure.data == ()
#     assert figure.layout.autosize is True
#     assert "xaxis" in figure.layout.scene
#     assert "yaxis" in figure.layout.scene
#     assert "zaxis" in figure.layout.scene
#     assert "aspectmode" in figure.layout.scene


@pytest.mark.parametrize("Backend", DEFAULT_ORBIT_PLOTTER_BACKENDS.values())
def test_set_different_attractor_raises_error(Backend):
    body1, body2 = Earth, Mars

    plotter = OrbitPlotter(backend=Backend())
    plotter.set_attractor(body1)

    with pytest.raises(NotImplementedError) as excinfo:
        plotter.set_attractor(body2)
    assert "Attractor has already been set to Earth" in excinfo.exconly()


@pytest.mark.parametrize("Backend", DEFAULT_ORBIT_PLOTTER_BACKENDS.values())
def test_plot_sets_attractor(Backend):
    plotter = OrbitPlotter(backend=Backend())
    assert plotter._attractor is None

    plotter.plot(iss)
    assert plotter._attractor == iss.attractor


@pytest.mark.parametrize("Backend", DEFAULT_ORBIT_PLOTTER_BACKENDS.values())
def test_plot_appends_data(Backend):
    plotter = OrbitPlotter(backend=Backend())
    assert len(plotter.trajectories) == 0

    plotter.plot(iss)
    assert len(plotter.trajectories) == 1


@pytest.mark.parametrize("Backend", DEFAULT_ORBIT_PLOTTER_BACKENDS.values())
def test_plot_coordinates_without_attractor_raises_error(Backend):
    plotter = OrbitPlotter(backend=Backend())

    with pytest.raises(ValueError) as excinfo:
        plotter._frame = 1  # Set it to something not None to skip frame check
        plotter.plot_coordinates({})
    assert (
        "An attractor must be set up first, please use "
        "set_attractor(Major_Body) or plot(orbit)" in excinfo.exconly()
    )


@pytest.mark.parametrize("Backend", DEFAULT_ORBIT_PLOTTER_BACKENDS_2D.values())
def test_plot_2d_trajectory_without_frame_raises_error(Backend):
    plotter = OrbitPlotter(backend=Backend())

    with pytest.raises(ValueError) as excinfo:
        plotter.set_attractor(Sun)
        plotter.plot_coordinates({})
    assert (
        "A frame must be set up first, please use "
        "set_orbit_frame(orbit) or plot(orbit)" in excinfo.exconly()
    )


def test_ephem_without_frame_raises_error():
    epochs = time.Time("2020-04-29 10:43", scale="tdb")
    earth = Ephem.from_body(Earth, epochs)
    plotter = OrbitPlotter()

    with pytest.raises(ValueError) as excinfo:
        plotter.set_attractor(Sun)
        plotter.plot_ephem(earth)
    assert (
        "A frame must be set up first, please use "
        "set_orbit_frame(orbit) or plot(orbit)" in excinfo.exconly()
    )


@pytest.mark.parametrize("Backend", DEFAULT_ORBIT_PLOTTER_BACKENDS_3D.values())
def test_plot_3d_trajectory_plots_a_trajectory(Backend):
    plotter = OrbitPlotter(backend=Backend())
    assert len(plotter.trajectories) == 0

    trajectory = churi.sample()
    plotter.set_attractor(Sun)
    plotter.plot_coordinates(trajectory)

    assert len(plotter.trajectories) == 1
    assert plotter._attractor == Sun


@pytest.mark.parametrize("Backend", DEFAULT_ORBIT_PLOTTER_BACKENDS_2D.values())
def test_plot_2d_trajectory_plots_a_trajectory(Backend):
    plotter = OrbitPlotter(backend=Backend())
    assert len(plotter.trajectories) == 0

    trajectory = churi.sample()
    plotter.set_attractor(Sun)
    plotter.set_orbit_frame(churi)
    plotter.plot_coordinates(trajectory)

    assert len(plotter.trajectories) == 1
    assert plotter._attractor == Sun


@pytest.mark.parametrize("Backend", DEFAULT_ORBIT_PLOTTER_BACKENDS_3D.values())
def test_set_view(Backend):
    plotter = OrbitPlotter(backend=Backend())
    plotter.set_view(0 * u.deg, 0 * u.deg, 1000 * u.m)
    plotter.show()

    eye = plotter.backend.figure["layout"]["scene"]["camera"]["eye"]
    assert eye["x"] == 1
    assert eye["y"] == 0
    assert eye["z"] == 0


@pytest.mark.parametrize(
    "is_dark, expected_bg",
    [(True, (0.0, 0.0, 0.0, 1.0)), (False, (1.0, 1.0, 1.0, 1))],
)
@pytest.mark.parametrize("MatplotlibBackend", [Matplotlib2D])
def test_dark_theme_backend_matplotlib(MatplotlibBackend, is_dark, expected_bg):
    backend = MatplotlibBackend(use_dark_theme=is_dark)
    plotter = OrbitPlotter(backend=backend)
    assert plotter.backend.scene.get_facecolor() == expected_bg
    assert plotter.backend.ax.get_facecolor() == expected_bg


@pytest.mark.parametrize("MatplotlibBackend", [Matplotlib2D])
def test_axes_labels_and_title(MatplotlibBackend):
    ax = plt.gca()
    backend = MatplotlibBackend(ax=ax)
    plotter = OrbitPlotter(backend=backend)
    ss = iss
    plotter.plot(ss)

    assert plotter.backend.ax.get_xlabel() == "$x$ (km)"
    assert plotter.backend.ax.get_ylabel() == "$y$ (km)"


def test_number_of_lines_for_osculating_orbit():
    op1 = OrbitPlotter()
    ss = iss

    l1 = op1.plot(ss)

    assert len(l1) == 2


def test_legend():
    op = OrbitPlotter()
    ss = iss
    op.plot(ss, label="ISS")
    legend = plt.gca().get_legend()

    ss.epoch.out_subfmt = "date_hm"
    label = f"{ss.epoch.iso} (ISS)"

    assert legend.get_texts()[0].get_text() == label


def test_color():
    op = OrbitPlotter()
    ss = iss
    c = "#FF0000"
    op.plot(ss, label="ISS", color=c)
    ax = plt.gca()

    assert ax.get_legend().get_lines()[0].get_c() == c
    for element in ax.get_lines():
        assert element.get_c() == c


def test_plot_coordinates_sets_label():
    expected_label = "67P"

    op = OrbitPlotter()
    trajectory = churi.sample()
    op.plot_body_orbit(Mars, J2000_TDB, label="Mars")

    op.plot_coordinates(trajectory, label=expected_label)

    legend = plt.gca().get_legend()
    assert legend.get_texts()[1].get_text() == expected_label


def test_redraw_makes_attractor_none():
    # TODO: Review
    op = OrbitPlotter()
    op._redraw()
    assert op._attractor_radius is not None


def test_set_frame_plots_same_colors():
    # TODO: Review
    op = OrbitPlotter()
    op.plot_body_orbit(Jupiter, J2000_TDB)
    colors1 = [orb[2] for orb in op.trajectories]
    op.set_body_frame(Jupiter)
    colors2 = [orb[2] for orb in op.trajectories]
    assert colors1 == colors2


def test_redraw_keeps_trajectories():
    # See https://github.com/hapsira/hapsira/issues/518
    op = OrbitPlotter()
    trajectory = churi.sample()
    op.plot_body_orbit(Mars, J2000_TDB, label="Mars")
    op.plot_coordinates(trajectory, label="67P")

    assert len(op.trajectories) == 2

    op.set_body_frame(Mars)

    assert len(op.trajectories) == 2


def test_plot_ephem_different_plane_raises_error():
    unused_epochs = Time.now().reshape(-1)
    unused_coordinates = CartesianRepresentation(
        [(1, 0, 0)] * u.au,
        xyz_axis=1,
        differentials=CartesianDifferential([(0, 1, 0)] * (u.au / u.day), xyz_axis=1),
    )

    op = OrbitPlotter(plane=Planes.EARTH_ECLIPTIC)
    op.set_attractor(Sun)
    op.set_body_frame(Earth)
    with pytest.raises(ValueError) as excinfo:
        op.plot_ephem(Ephem(unused_epochs, unused_coordinates, Planes.EARTH_EQUATOR))

    assert (
        "sample the ephemerides using a different plane or create a new plotter"
        in excinfo.exconly()
    )


@pytest.mark.mpl_image_compare
def test_basic_plotting():
    fig, ax = plt.subplots()
    backend = Matplotlib2D(ax=ax)
    plotter = OrbitPlotter(backend=backend)
    plotter.plot(iss)

    return fig


@pytest.mark.mpl_image_compare
def test_basic_trajectory_plotting():
    fig, ax = plt.subplots()
    backend = Matplotlib2D(ax=ax)
    plotter = OrbitPlotter(backend=backend)
    plotter.set_attractor(Earth)
    plotter.set_orbit_frame(iss)
    plotter.plot_coordinates(iss.sample())

    return fig


@pytest.mark.mpl_image_compare
def test_basic_orbit_and_trajectory_plotting():
    fig, ax = plt.subplots()
    backend = Matplotlib2D(ax=ax)
    plotter = OrbitPlotter(backend=backend)
    plotter.plot(iss)
    plotter.plot_coordinates(molniya.sample(), label="Molniya")

    return fig


@pytest.mark.mpl_image_compare
def test_trail_plotting():
    fig, ax = plt.subplots()
    backend = Matplotlib2D(ax=ax)
    plotter = OrbitPlotter(backend=backend)
    plotter.plot(iss, trail=True)

    return fig


@pytest.mark.mpl_image_compare
def test_plot_different_planes():
    fig, ax = plt.subplots()
    backend = Matplotlib2D(ax=ax)
    plotter = OrbitPlotter(backend=backend)
    plotter.plot(iss)
    plotter.plot(molniya.change_plane(Planes.EARTH_ECLIPTIC))

    return fig


@pytest.mark.mpl_image_compare
def test_body_plotting(earth_perihelion):
    Earth.plot(epoch=earth_perihelion)

    return plt.gcf()


@pytest.mark.mpl_image_compare
@pytest.mark.remote_data
def test_plot_ephem_epoch():
    epoch = Time("2020-02-14 00:00:00")
    ephem = Ephem.from_horizons(
        "2020 CD3",
        time_range(Time("2020-02-13 12:00:00"), end=Time("2020-02-14 12:00:00")),
        attractor=Earth,
    )

    fig, ax = plt.subplots()
    backend = Matplotlib2D(ax=ax)
    plotter = OrbitPlotter(backend=backend)
    plotter.set_attractor(Earth)
    plotter.set_orbit_frame(Orbit.from_ephem(Earth, ephem, epoch))

    plotter.plot_ephem(ephem, epoch, label="2020 CD3 Minimoon", color="k")

    return fig


@pytest.mark.mpl_image_compare
@pytest.mark.remote_data
def test_plot_ephem_no_epoch():
    epoch = Time("2020-02-14 00:00:00")
    ephem = Ephem.from_horizons(
        "2020 CD3",
        time_range(Time("2020-02-13 12:00:00"), end=Time("2020-02-14 12:00:00")),
        attractor=Earth,
    )

    fig, ax = plt.subplots()
    backend = Matplotlib2D(ax=ax)
    plotter = OrbitPlotter(backend=backend)
    plotter.set_attractor(Earth)
    plotter.set_orbit_frame(Orbit.from_ephem(Earth, ephem, epoch))

    plotter.plot_ephem(ephem, label="2020 CD3 Minimoon", color="k")

    return fig


def test_body_frame_raises_warning_if_time_is_not_tdb_with_proper_time(
    recwarn,
):
    from hapsira.warnings import TimeScaleWarning

    body = Jupiter
    epoch = Time("2017-09-29 07:31:26", scale="utc")
    expected_epoch_string = "2017-09-29 07:32:35.182"  # epoch.tdb.value

    op = OrbitPlotter()
    op.set_body_frame(body, epoch)

    w = recwarn.pop(TimeScaleWarning)

    assert expected_epoch_string in str(w.message)


@pytest.mark.xfail(sys.maxsize < 2**32, reason="not supported for 32 bit systems")
@pytest.mark.mpl_image_compare
def test_plot_maneuver_using_matplotlib2D_backend():
    # Data from Vallado, example 6.1
    alt_i = 191.34411 * u.km
    alt_f = 35781.34857 * u.km
    _a = 0 * u.deg
    orb_i = Orbit.from_classical(
        attractor=Earth,
        a=Earth.R + alt_i,
        ecc=0 * u.one,
        inc=_a,
        raan=_a,
        argp=_a,
        nu=_a,
    )

    # Create the maneuver
    man = Maneuver.hohmann(orb_i, Earth.R + alt_f)

    # Plot the maneuver
    fig, ax = plt.subplots()
    backend = Matplotlib2D(ax=ax)
    plotter = OrbitPlotter(backend=backend)
    plotter.plot(orb_i, label="Initial orbit", color="blue")
    plotter.plot_maneuver(orb_i, man, label="Hohmann maneuver", color="red")

    return fig
