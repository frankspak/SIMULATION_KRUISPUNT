import numpy as np
from window import *
from verkeerslicht import *
from simulation import *
from voertuig import *
from voertuig_generator import *
from weg import *
from bocht import *

sim = Simulation()

# Play with these
n = 15
a = 2
b = 12
l = 300

# Nodes
WEST_RECHTS_BEGIN = (-b-l, a)
WEST_LINKS_BEGIN =	(-b-l, -a)

ZUID_RECHTS_BEGIN = (a, b+l)
ZUID_LINKS_BEGIN = (-a, b+l)

OOST_RECHTS_BEGIN = (b+l, -a)
OOST_LINKS_BEGIN = (b+l, a)

NOORD_RECHTS_BEGIN = (-a, -b-l)
NOORD_LINKS_BEGIN = (a, -b-l)


WEST_RECHTS = (-b, a)
WEST_LINKS = (-b, -a)

ZUID_RECHTS = (a, b)
ZUID_LINKS = (-a, b)

OOST_RECHTS = (b, -a)
OOST_LINKS = (b, a)

NOORD_RECHTS = (-a, -b)
NOORD_LINKS = (a, -b)

# Roads
WESTEN_BINNENKOMEND = (WEST_RECHTS_BEGIN, WEST_RECHTS)
ZUIDEN_INKOMEND = (ZUID_RECHTS_BEGIN, ZUID_RECHTS)
OOST_INKOMEND = (OOST_RECHTS_BEGIN, OOST_RECHTS)
NOORD_INKOMEND = (NOORD_RECHTS_BEGIN, NOORD_RECHTS)

WEST_UITGANG = (WEST_LINKS, WEST_LINKS_BEGIN)
ZUID_UITGAAND = (ZUID_LINKS, ZUID_LINKS_BEGIN)
OOST_UITGANG = (OOST_LINKS, OOST_LINKS_BEGIN)
NOORD_UITGAAND = (NOORD_LINKS, NOORD_LINKS_BEGIN)

WESTEN_RECHT = (WEST_RECHTS, OOST_LINKS)
ZUID_RECHT = (ZUID_RECHTS, NOORD_LINKS)
OOST_RECHT = (OOST_RECHTS, WEST_LINKS)
NOORD_RECHT = (NOORD_RECHTS, ZUID_LINKS)

WEST_RECHTS_DRAAIEN = weg_afslaan(WEST_RECHTS, ZUID_LINKS, SLA_RECHTSAF, n)
WESTEN_LINKS_DRAAIEN = weg_afslaan(WEST_RECHTS, NOORD_LINKS, SLA_LINKSAF, n)

ZUID_RECHTS_DRAAIEN = weg_afslaan(ZUID_RECHTS, OOST_LINKS, SLA_RECHTSAF, n)
ZUID_LINKS_DRAAIEN = weg_afslaan(ZUID_RECHTS, WEST_LINKS, SLA_LINKSAF, n)

OOST_RECHTS_DRAAIEN = weg_afslaan(OOST_RECHTS, NOORD_LINKS, SLA_RECHTSAF, n)
OOST_LINKS_DRAAIEN = weg_afslaan(OOST_RECHTS, ZUID_LINKS, SLA_LINKSAF, n)

NOORD_RECHTS_DRAAIEN = weg_afslaan(NOORD_RECHTS, WEST_LINKS, SLA_RECHTSAF, n)
NOORD_LINKS_DRAAIEN = weg_afslaan(NOORD_RECHTS, OOST_LINKS, SLA_LINKSAF, n)

sim.wegen_maken([
    WESTEN_BINNENKOMEND,
    ZUIDEN_INKOMEND,
    OOST_INKOMEND,
    NOORD_INKOMEND,

    WEST_UITGANG,
    ZUID_UITGAAND,
    OOST_UITGANG,
    NOORD_UITGAAND,

    WESTEN_RECHT,
    ZUID_RECHT,
    OOST_RECHT,
    NOORD_RECHT,

    *WEST_RECHTS_DRAAIEN,
    *WESTEN_LINKS_DRAAIEN,

    *ZUID_RECHTS_DRAAIEN,
    *ZUID_LINKS_DRAAIEN,

    *OOST_RECHTS_DRAAIEN,
    *OOST_LINKS_DRAAIEN,

    *NOORD_RECHTS_DRAAIEN,
    *NOORD_LINKS_DRAAIEN
])

def road(a): return range(a, a+n)

sim.create_gen({
'voertuig_tarief': 30,
'voertuigen':[
    [3, {'path': [0, 8, 6]}],
    [1, {'path': [0, *road(12), 5]}],
    [1, {'path': [0, *road(12+n), 7]}],

    [3, {'path': [1, 9, 7]}],
    [1, {'path': [1, *road(12+2*n), 6]}],
    [1, {'path': [1, *road(12+3*n), 4]}],


    [3, {'path': [2, 10, 4]}],
    [1, {'path': [2, *road(12+4*n), 7]}],
    [1, {'path': [2, *road(12+5*n), 5]}],

    [3, {'path': [3, 11, 5]}],
    [1, {'path': [3, *road(12+6*n), 4]}],
    [1, {'path': [3, *road(12+7*n), 6]}]
]})

sim.create_signal([[0, 2], [1, 3]])


# Start simulation
win = Window(sim)
win.zoom = 10
win.run(stappen_per_update=10)