class Verkeerslicht:
    def __init__(self, wegen, config={}):
        # Wegen initialiseren
        self.wegen = wegen
        # Standaard configuratie instellen
        self.set_default_config()
        # Update configuratie
        for attr, val in config.items():
            setattr(self, attr, val)
        # bereken properties
        self.init_properties()

    def set_default_config(self):
        self.cycle = [(True, False), (False, True)]
        self.langzame_afstand = 45
        self.langzame_factor = 0.3
        self.stop_afstand = 10
        self.satus = 0

        self.huidige_cyclusindex = 0

        self.last_t = 0

    def init_properties(self):
        for i in range(len(self.wegen)):
            for weg in self.wegen[i]:
                weg.verkeerslicht_instellen(self, i)

    @property
    def huidige_cyclus(self):
        return self.cycle[self.huidige_cyclusindex]
    
    def update(self, sim):
        cycle_lengte = 30
        k = (sim.t // cycle_lengte) % 2
        self.huidige_cyclusindex = int(k)

