from scipy.spatial import distance
from collections import deque

class Weg:
    def __init__(self, start, eind):
        self.start = start
        self.eind = eind

        self.voertuigen = deque()

        self.init_properties()

    def init_properties(self):
        self.lengte = distance.euclidean(self.start, self.eind)
        self.hoek_sin = (self.eind[1]-self.start[1]) / self.lengte
        self.hoek_cos = (self.eind[0]-self.start[0]) / self.lengte
        # self.angle = np.arctan2(self.end[1]-self.start[1], self.end[0]-self.start[0])
        self.heeft_verkeerslicht = False

    def verkeerslicht_instellen(self, signal, group):
        self.verkeerslicht = signal
        self.verkeerslicht_group = group
        self.heeft_verkeerslicht = True

    @property
    def verkeerslicht_staat(self):
        if self.heeft_verkeerslicht:
            i = self.verkeerslicht_group
            return self.verkeerslicht.huidige_cyclus[i]
        return True

    def update(self, dt):
        n = len(self.voertuigen)

        if n > 0:
            # Update eerste voertuig
            self.voertuigen[0].update(None, dt)
            # Update andere voertuigen
            for i in range(1, n):
                lead = self.voertuigen[i-1]
                self.voertuigen[i].update(lead, dt)

             # Controleer op verkeerslicht
            if self.verkeerslicht_staat:
                # Als verkeerslicht groen is of niet bestaat
                # Laat dan voertuigen gaan
                self.voertuigen[0].ontstoppen()
                for voertuig in self.voertuigen:
                    voertuig.niet_vertragen()
            else:
                # Als het verkeerslicht rood is
                if self.voertuigen[0].x >= self.lengte - self.verkeerslicht.langzame_afstand:
                    # Langzame voertuigen in vertragingszone
                    self.voertuigen[0].langzaam(self.verkeerslicht.langzame_factor*self.voertuigen[0]._v_max)
                if self.voertuigen[0].x >= self.lengte - self.verkeerslicht.stop_afstand and\
                   self.voertuigen[0].x <= self.lengte - self.verkeerslicht.stop_afstand / 2:
                    # Stop voertuigen in de stopzone
                    self.voertuigen[0].stop()
