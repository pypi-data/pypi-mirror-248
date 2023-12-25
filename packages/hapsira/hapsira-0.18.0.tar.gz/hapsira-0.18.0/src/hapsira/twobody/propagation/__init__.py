"""The following script holds the different high level functions for the
different propagators available at hapsira:

+-------------+------------+-----------------+-----------------+
|  Propagator | Elliptical |    Parabolic    |    Hyperbolic   |
+-------------+------------+-----------------+-----------------+
|  farnocchia |      ✓     |        ✓        |        ✓        |
+-------------+------------+-----------------+-----------------+
|   vallado   |      ✓     |        ✓        |        ✓        |
+-------------+------------+-----------------+-----------------+
|   mikkola   |      ✓     |        ✓        |        ✓        |
+-------------+------------+-----------------+-----------------+
|   markley   |      ✓     |        x        |        x        |
+-------------+------------+-----------------+-----------------+
|   pimienta  |      ✓     |        ✓        |        x        |
+-------------+------------+-----------------+-----------------+
|   gooding   |      ✓     |        x        |        x        |
+-------------+------------+-----------------+-----------------+
|    danby    |      ✓     |        ✓        |        ✓        |
+-------------+------------+-----------------+-----------------+
|    cowell   |      ✓     |        ✓        |        ✓        |
+-------------+------------+-----------------+-----------------+
|  recseries  |      ✓     |        x        |        x        |
+-------------+------------+-----------------+-----------------+

"""
from hapsira.twobody.propagation.cowell import CowellPropagator
from hapsira.twobody.propagation.danby import DanbyPropagator
from hapsira.twobody.propagation.enums import PropagatorKind
from hapsira.twobody.propagation.farnocchia import FarnocchiaPropagator
from hapsira.twobody.propagation.gooding import GoodingPropagator
from hapsira.twobody.propagation.markley import MarkleyPropagator
from hapsira.twobody.propagation.mikkola import MikkolaPropagator
from hapsira.twobody.propagation.pimienta import PimientaPropagator
from hapsira.twobody.propagation.recseries import RecseriesPropagator
from hapsira.twobody.propagation.vallado import ValladoPropagator

from ._compat import propagate

ALL_PROPAGATORS = [
    CowellPropagator,
    DanbyPropagator,
    FarnocchiaPropagator,
    GoodingPropagator,
    MarkleyPropagator,
    MikkolaPropagator,
    PimientaPropagator,
    RecseriesPropagator,
    ValladoPropagator,
]
ELLIPTIC_PROPAGATORS = [
    propagator
    for propagator in ALL_PROPAGATORS
    if propagator.kind & PropagatorKind.ELLIPTIC
]
PARABOLIC_PROPAGATORS = [
    propagator
    for propagator in ALL_PROPAGATORS
    if propagator.kind & PropagatorKind.PARABOLIC
]
HYPERBOLIC_PROPAGATORS = [
    propagator
    for propagator in ALL_PROPAGATORS
    if propagator.kind & PropagatorKind.HYPERBOLIC
]


__all__ = [item.__name__ for item in ALL_PROPAGATORS] + ["propagate"]
