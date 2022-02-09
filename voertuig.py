import numpy as np

class Voertuigen:
    def __init__(self, config={}):
        # Standaardconfiguratie instellen
        self.set_default_config()

        #Update configuratie
        for attr, val in config.items():
            setattr(self, attr, val)

        # Bereken properties
        self.init_properties()

    def set_default_config(self):    
        self.l = 4
        self.s0 = 4
        self.T = 1
        self.v_max = 16.6
        self.a_max = 1.44
        self.b_max = 4.61

        self.path = []
        self.huidige_wegenindex = 0

        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.gestopt = False

    def init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max

    def update(self, lead, dt):
        # Update positie en snelheid
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Acceleratie updaten
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.gestopt:
            self.a = -self.b_max*self.v/self.v_max
        
    def stop(self):
        self.gestopt = True

    def ontstoppen(self):
        self.gestopt = False

    def langzaam(self, v):
        self.v_max = v

    def niet_vertragen(self):
        self.v_max = self._v_max
        

