def bocht_punten(start, eind, control, resolution=5):
	# Als curve een rechte lijn is
	if (start[0] - eind[0])*(start[1] - eind[1]) == 0:
		return [start, eind]

	#Zo niet, retourneer dan een curve
	path = []

	for i in range(resolution+1):
		t = i/resolution
		x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 *eind[0]
		y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 *eind[1]
		path.append((x, y))

	return path

def bocht_weg(start, eind, control, resolution=15):
	punten = bocht_punten(start, eind, control, resolution=resolution)
	return [(punten[i-1], punten[i]) for i in range(1, len(punten))]

SLA_LINKSAF = 0
SLA_RECHTSAF = 1
def weg_afslaan(start, eind, draai_richting, resolution=15):
	# Krijg controlepunt
	x = min(start[0], eind[0])
	y = min(start[1], eind[1])

	if draai_richting == SLA_LINKSAF:
		control = (
			x - y + start[1],
			y - x + eind[0]
		)
	else:
		control = (
			x - y + eind[1],
			y - x + start[0]
		)
	
	return bocht_weg(start, eind, control, resolution=resolution)

