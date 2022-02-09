from voertuig import Voertuigen
from numpy.random import randint

class Voertuiggenerator:
    def __init__(self, sim, config={}):
        self.sim = sim

        # Standaardconfiguraties instellen
        self.set_default_config()

        # update configuraties
        for attr, val in config.items():
            setattr(self, attr, val)

        # bereken properties
        self.init_properties()

    def set_default_config(self):
        """Standaardconfiguratie instellen"""
        self.voertuig_tarief = 20
        self.voertuigen = [
            (1, {})
        ]
        self.laatst_toegevoegde_tijd = 0

    def init_properties(self):
        self.aankomend_voertuig = self.voertuig_genereren()

    def voertuig_genereren(self):
        """Retourneert een willekeurig voertuig van zelf.voertuigen met willekeurige verhoudingen"""
        totaal = sum(pair[0] for pair in self.voertuigen)
        r = randint(1, totaal+1)
        for (weight, config) in self.voertuigen:
            r -= weight
            if r <= 0:
                return Voertuigen(config)

    def update(self):
        """Voertuigen toevoegen"""
        if self.sim.t - self.laatst_toegevoegde_tijd >= 60 / self.voertuig_tarief:
            # Als de tijd is verstreken nadat het laatst toegevoegde voertuig is
            # langer dan voertuigperiode; een voertuig genereren
            weg = self.sim.wegen[self.aankomend_voertuig.path[0]]
            if len(weg.voertuigen) == 0\
               or weg.voertuigen[-1].x > self.aankomend_voertuig.s0 + self.aankomend_voertuig.l:
                # Als er ruimte is voor het gegenereerde voertuig; voeg het toe
                self.aankomend_voertuig.time_added = self.sim.t
                weg.voertuigen.append(self.aankomend_voertuig)
                # Reset laatst toegevoegde tijd en aankomend voertuig
                self.laatst_toegevoegde_tijd = self.sim.t
            self.aankomend_voertuig = self.voertuig_genereren()

