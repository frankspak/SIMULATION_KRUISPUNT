import pygame
from pygame import gfxdraw
import numpy as np

class Window:
    def __init__(self, sim, config={}):
        # Simulatie om te tekenen
        self.sim = sim

        # Standaardconfiguraties instellen
        self.set_default_config()

        # Configuraties bijwerken
        for attr, val in config.items():
            setattr(self, attr, val)
        
    def set_default_config(self):
        """Standaardconfiguratie instellen"""
        self.width = 500
        self.height = 400
        self.bg_kleur = (150, 250, 150)

        self.fps = 60
        self.zoom = 5
        self.offset = (0, 0)

        self.mouse_last = (0, 0)
        self.mouse_down = False


    def loop(self, loop=None):
        """Toont een venster waarin de simulatie wordt gevisualiseerd en voert de loop uit."""
        
        # Een pygame window maken
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()

        # Vaste FPS
        clock = pygame.time.Clock()

        # Tekst tekenen
        pygame.font.init()
        self.text_font = pygame.font.SysFont('Lucida Console', 16)

        #loop tekenen
        running = True
        while running:
            # Simulatie updaten:
            if loop: loop(self.sim)

            # Simulatie tekenen
            self.draw()

            # Update window
            pygame.display.update()
            clock.tick(self.fps)

            # Alle gebeurtenissen afhandelen
            for event in pygame.event.get():
                # Sluit het programma af als het Window is gesloten
                if event.type == pygame.QUIT:
                    running = False
                # Muisgebeurtenissen afhandelen
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Als muisknop omlaag
                    if event.button == 1:
                        # Links klikken
                        x, y = pygame.mouse.get_pos()
                        x0, y0 = self.offset
                        self.mouse_last = (x-x0*self.zoom, y-y0*self.zoom)
                        self.mouse_down = True
                    if event.button == 4:
                        # Muiswiel omhoog
                        self.zoom *=  (self.zoom**2+self.zoom/4+1) / (self.zoom**2+1)
                    if event.button == 5:
                        # Muiswiel omlaag
                        self.zoom *= (self.zoom**2+1) / (self.zoom**2+self.zoom/4+1)
                elif event.type == pygame.MOUSEMOTION:
                    # Inhoud slepen
                    if self.mouse_down:
                        x1, y1 = self.mouse_last
                        x2, y2 = pygame.mouse.get_pos()
                        self.offset = ((x2-x1)/self.zoom, (y2-y1)/self.zoom)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False           

    def run(self, stappen_per_update=1):
        """Voert de simulatie uit door bij elke loop te updaten."""
        def loop(sim):
            sim.run(stappen_per_update)
        self.loop(loop)

    def convert(self, x, y=None):
        """Converteert simulatiecoördinaten naar schermcoördinaten"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(self.width/2 + (x + self.offset[0])*self.zoom),
            int(self.height/2 + (y + self.offset[1])*self.zoom)
        )

    def inverse_convert(self, x, y=None):
        """Converteert schermcoördinaten naar simulatiecoördinaten"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(-self.offset[0] + (x - self.width/2)/self.zoom),
            int(-self.offset[1] + (y - self.height/2)/self.zoom)
        )


    def background(self, r, g, b):
        """Vult het scherm met één kleur."""
        self.screen.fill((r, g, b))

    def line(self, start_pos, eind_pos, kleur):
        """Trekt een lijn."""
        gfxdraw.line(
            self.screen,
            *start_pos,
            *eind_pos,
            kleur
        )

    def rect(self, pos, size, kleur):
        """Tekent een rechthoek."""
        gfxdraw.rectangle(self.screen, (*pos, *size), kleur)

    def box(self, pos, size, kleur):
        gfxdraw.box(self.screen, (*pos, *size), kleur)

    def circle(self, pos, straal, kleur, filled=True):
        gfxdraw.aacircle(self.screen, *pos, straal, kleur)
        if filled:
            gfxdraw.filled_circle(self.screen, *pos, straal, kleur)



    def polygon(self, vertices, kleur, filled=True):
        gfxdraw.aapolygon(self.screen, vertices, kleur)
        if filled:
            gfxdraw.filled_polygon(self.screen, vertices, kleur)

    def rotated_box(self, pos, size, angle=None, cos=None, sin=None, centered=True, kleur=(50, 50, 50), filled=True):
        """Tekent een rechthoek in het midden op *pos* met afmeting *size* tegen de klok in gedraaid met *hoek*."""
        x, y = pos
        l, h = size

        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        
        vertex = lambda e1, e2: (
            x + (e1*l*cos + e2*h*sin)/2,
            y + (e1*l*sin - e2*h*cos)/2
        )

        if centered:
            vertices = self.convert(
                [vertex(*e) for e in [(-1,-1), (-1, 1), (1,1), (1,-1)]]
            )
        else:
            vertices = self.convert(
                [vertex(*e) for e in [(0,-1), (0, 1), (2,1), (2,-1)]]
            )

        self.polygon(vertices, kleur, filled=filled)

    def rotated_rect(self, pos, size, angle=None, cos=None, sin=None, centered=True, kleur=(0, 0, 255)):
        self.rotated_box(pos, size, angle=angle, cos=cos, sin=sin, centered=centered, kleur=kleur, filled=False)

    def arrow(self, pos, size, angle=None, cos=None, sin=None, kleur=(170, 150, 190)):
        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        
        self.rotated_box(
            pos,
            size,
            cos=(cos - sin) / np.sqrt(2),
            sin=(cos + sin) / np.sqrt(2),
            kleur=kleur,
            centered=False
        )

        self.rotated_box(
            pos,
            size,
            cos=(cos + sin) / np.sqrt(2),
            sin=(sin - cos) / np.sqrt(2),
            kleur=kleur,
            centered=False
        )


    def draw_axes(self, kleur=(70, 70, 70)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)
        self.line(
            self.convert((0, y_start)),
            self.convert((0, y_end)),
            kleur
        )
        self.line(
            self.convert((x_start, 0)),
            self.convert((x_end, 0)),
            kleur
        )

    def draw_grid(self, unit=50, kleur=(150,150,150)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)

        n_x = int(x_start / unit)
        n_y = int(y_start / unit)
        m_x = int(x_end / unit)+1
        m_y = int(y_end / unit)+1

        for i in range(n_x, m_x):
            self.line(
                self.convert((unit*i, y_start)),
                self.convert((unit*i, y_end)),
                kleur
            )
        for i in range(n_y, m_y):
            self.line(
                self.convert((x_start, unit*i)),
                self.convert((x_end, unit*i)),
                kleur
            )

    def draw_roads(self):
        for weg in self.sim.wegen:
            # Teken weg achtergrond
            self.rotated_box(
                weg.start,
                (weg.lengte, 3.7),
                cos=weg.hoek_cos,
                sin=weg.hoek_sin,
                kleur=(80, 80, 220),
                centered=False
            )
            # Draw road lines
            # self.rotated_box(
            #     weg.start,
            #     (weg.length, 0.25),
            #     cos=weg.angle_cos,
            #     sin=weg.angle_sin,
            #     color=(0, 0, 0),
            #     centered=False
            # )

            # Teken wegpijl
            if weg.lengte > 5:
                for i in np.arange(-0.5*weg.lengte, 0.5*weg.lengte, 10):
                    pos = (
                        weg.start[0] + (weg.lengte/2 + i + 3) * weg.hoek_cos,
                        weg.start[1] + (weg.lengte/2 + i + 3) * weg.hoek_sin
                    )

                    self.arrow(
                        pos,
                        (-1.25, 0.2),
                        cos=weg.hoek_cos,
                        sin=weg.hoek_sin
                    )   
            




    def draw_vehicle(self, voertuig, weg):
        l, h = voertuig.l,  2
        sin, cos = weg.hoek_sin, weg.hoek_cos

        x = weg.start[0] + cos * voertuig.x
        y = weg.start[1] + sin * voertuig.x

        self.rotated_box((x, y), (l, h), cos=cos, sin=sin, centered=True)

    def draw_vehicles(self):
        for weg in self.sim.wegen:
            # Draw vehicles
            for voertuig in weg.voertuigen:
                self.draw_vehicle(voertuig, weg)

    def draw_signals(self):
        for signal in self.sim.verkeerssignalen:
            for i in range(len(signal.wegen)):
                kleur = (0, 255, 0) if signal.huidige_cyclus[i] else (255, 0, 0)
                for weg in signal.wegen[i]:
                    a = 0
                    position = (
                        (1-a)*weg.eind[0] + a*weg.start[0],
                        (1-a)*weg.eind[1] + a*weg.start[1]
                    )
                    self.rotated_box(
                        position,
                        (1, 3),
                        cos=weg.hoek_cos, sin=weg.hoek_sin,
                        kleur=kleur)

    def draw_status(self):
        text_fps = self.text_font.render(f't={self.sim.t:.5}', False, (0, 0, 0))
        text_frc = self.text_font.render(f'n={self.sim.aantal_frames}', False, (0, 0, 0))
        
        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_frc, (100, 0))


    def draw(self):
        # Achtergrond vullen
        self.background(*self.bg_kleur)

        # Major and minor grid and axes
        # self.draw_grid(10, (220,220,220))
        # self.draw_grid(100, (200,200,200))
        # self.draw_axes()

        self.draw_roads()
        self.draw_vehicles()
        self.draw_signals()

        # Draw status info
        self.draw_status()
        