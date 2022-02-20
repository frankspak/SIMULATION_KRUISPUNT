from weg import Weg
from copy import deepcopy
from voertuig_generator import Voertuiggenerator
from verkeerslicht import Verkeerslicht

class Simulation:
    def __init__(self, config={}):
        # Standaardconfiguratie instellen
        self.set_default_config()

        # Update configuratie
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0            # Tijd bijhouden
        self.aantal_frames = 0    # Frame telling bijhouden
        self.dt = 1/90        #  Simulatie tijdstap
        self.wegen = []         #  Array om wegen op te slaan
        self.generators = []
        self.verkeerssignalen = []

    def weg_maken(self, start, eind):
        weg = Weg(start, eind)
        self.wegen.append(weg)
        return weg

    def wegen_maken(self, wegenlijst):
        for weg in wegenlijst:
            self.weg_maken(*weg)

    def create_gen(self, config={}):
        gen = Voertuiggenerator(self, config)
        self.generators.append(gen)
        return gen

    def create_signal(self, wegen, config={}):
        weg_strook = [[self.wegen[i] for i in road_group] for road_group in wegen]
        sig = Verkeerslicht(weg_strook, config)
        self.verkeerssignalen.append(sig)
        return sig

    def update(self):
        # Update elke weg
        for weg in self.wegen:
            weg.update(self.dt)

        # Voertuigen toevoegen
        for gen in self.generators:
            gen.update()

        for signal in self.verkeerssignalen:
            signal.update(self)

        # Controleer wegen voor voertuigen buiten de grenzen
        for weg in self.wegen:
            # weg heeft geen voertuigen, ga verder
            if len(weg.voertuigen) == 0: continue
            # Als niet
            voertuig = weg.voertuigen[0]
            # Als het eerste voertuig zich buiten de weg bevindt
            if voertuig.x >= weg.lengte:
                # Als het voertuig een volgende weg heeft:
                if voertuig.huidige_wegenindex + 1 < len(voertuig.path):
                    # Actualiseren huidige weg naar volgende weg
                    voertuig.huidige_wegenindex += 1
                    # Maak een kopie en reset enkele voertuigeigenschappen
                    new_voertuig = deepcopy(voertuig)
                    new_voertuig.x = 0
                    # Voeg het toe aan de volgende weg
                    volgende_wegindex = voertuig.path[voertuig.huidige_wegenindex]
                    self.wegen[volgende_wegindex].voertuigen.append(new_voertuig)
                # Verwijder het in alle gevallen van de weg
                weg.voertuigen.popleft()
        # Tijd verhogen
        self.t += self.dt
        self.aantal_frames += 1


    def run(self, steps):
        for _ in range(steps):
            self.update()