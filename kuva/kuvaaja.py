# -*- coding: UTF-8 -*-

from kuva import *

# Mahdolliset viiva- ja labelvälit.
valit = []
for i in range(-10, 11):
	if i < 0:
		b = 10.**i
	else:
		b = 10**i
	valit.append(b)
	valit.append(2 * b)
	valit.append(5 * b)

def pohja(minX, maxX, minY, maxY, leveys = None, korkeus = None, nimiX = "", nimiY = "", ruudukko = True):
	"""Luo kuvaajapohja kuvaajalle jossa X-koordinaatit ovat välillä [minX, maxX]
	ja Y-koordinaatit välillä [minY, maxY]. Kuvaajapohjan koko on
	'leveys' x 'korkeus'. Mikäli vain toinen parametreista 'leveys' ja 'korkeus'
	puuttuu, se lasketaan toisen perusteella säilyttäen kuvasuhteen. Mikäli
	molemmat puuttuvat, tehdään kuvaajapohjasta saman kokoinen kuin
	koordinaattialoista. On oltava minX <= 0 <= maxX ja minY <= 0 <= maxY.
	Kuvaajapohja rajoittaa piirron alueelle [minX, maxX] x [minY, maxY].
	nimiX:llä ja nimiY:llä voidaan nimetä akselit.
	Pohjaan piirretään ruudukko jos 'ruudukko' on True."""
	
	ret = AsetusPalautin()
	
	if minX > 0 or maxX < 0 or minY > 0 or maxY < 0:
		raise ValueError("kuvaajapohja: On oltava minX <= 0 <= maxX ja minY <= 0 <= maxY.")
	
	if minX == maxX or minY == maxY:
		raise ValueError("kuvaajapohja: On oltava minX < maxX ja minY < maxY.")
	
	dX = maxX - minX
	dY = maxY - minY
	maxX += 1e-5 * dX
	minX -= 1e-5 * dX
	maxY += 1e-5 * dY
	minY -= 1e-5 * dY
	
	if leveys is None and korkeus is None:
		leveys = maxX - minX
		korkeus = maxY - minY
	
	if leveys is None:
		leveys = (maxX - minX) * float(korkeus) / (maxY - minY)
	
	if korkeus is None:
		korkeus = (maxY - minY) * float(leveys) / (maxX - minX)
	
	leveys = float(leveys)
	korkeus = float(korkeus)
	
	# Siirrytään uuden kuvaajan koordinaatteihin.
	skaalaaX(leveys / (maxX - minX))
	skaalaaY(korkeus / (maxY - minY))
	
	siirraX(minX)
	siirraY(minY)
	
	# Piirretään ruudukko.
	for vali in valit:
		xvali = vali
		if xvali * tila.asetukset['xmuunnos'][0] > 0.42: break
	for vali in valit:
		yvali = vali
		if yvali * tila.asetukset['ymuunnos'][0] > 0.42: break
	if ruudukko:
		vari = "black!30!white"
		
		def piirraPystyviiva(X):
			alku = muunna((X, minY))
			loppu = muunna((X, maxY))
			tila.out.write("\\draw[color={}] {} -- {};\n".format(vari, tikzPiste(alku), tikzPiste(loppu)))
		
		def piirraVaakaviiva(Y):
			alku = muunna((minX, Y))
			loppu = muunna((maxX, Y))
			tila.out.write("\\draw[color={}] {} -- {};\n".format(vari, tikzPiste(alku), tikzPiste(loppu)))
		
		X = xvali
		while X < maxX:
			piirraPystyviiva(X)
			X += xvali
		X = -xvali
		while X > minX:
			piirraPystyviiva(X)
			X -= xvali
		Y = yvali
		while Y < maxY:
			piirraVaakaviiva(Y)
			Y += yvali
		Y = -yvali
		while Y > minY:
			piirraVaakaviiva(Y)
			Y -= yvali
	
	# Piirretään pohjaristi.
	nuoli = "\\draw[arrows=-triangle 45, thick, color=black] {} -- {};\n"
	valku = vekSumma(muunna((minX, 0)), (-0.2, 0))
	vloppu = vekSumma(muunna((maxX, 0)), (0.9, 0))
	vlopput = vekSumma(muunna((maxX, 0)), (0.6, 0))
	palku = vekSumma(muunna((0, minY)), (0, -0.2))
	ploppu = vekSumma(muunna((0, maxY)), (0, 0.6))
	tila.out.write("\\draw[arrows=-triangle 45, thick, color=black] {} -- {};\n".format(tikzPiste(valku), tikzPiste(vloppu)))
	tila.out.write("\\draw[color=black] {} node[above right] {{{}}};\n".format(tikzPiste(vlopput), nimiX))
	tila.out.write("\\draw[arrows=-triangle 45, thick, color=black] {} -- {} node[right] {{{}}};\n".format(tikzPiste(palku), tikzPiste(ploppu), nimiY))
	
	# Piirretään asteikko.
	def piirraXKohta(X):
		alku = vekSumma(muunna((X, 0)), (0, -0.09))
		kohta = vekSumma(muunna((X, 0)), (-0.08, 0))
		loppu = vekSumma(muunna((X, 0)), (0, 0.09))
		tila.out.write("\\draw[line width=1.2pt, color=black] {} -- {};\n".format(tikzPiste(alku), tikzPiste(loppu)))
		tila.out.write("\\draw[color=black] {} node[above right] {{\\footnotesize {}}};\n".format(tikzPiste(kohta), X))
	
	def piirraYKohta(Y):
		alku = vekSumma(muunna((0, Y)), (-0.09, 0))
		kohta = muunna((0, Y))
		loppu = vekSumma(muunna((0, Y)), (0.09, 0))
		tila.out.write("\\draw[line width=1.2pt, color=black] {} -- {};\n".format(tikzPiste(alku), tikzPiste(loppu)))
		tila.out.write("\\draw[color=black] {} node[right] {{\\footnotesize {}}};\n".format(tikzPiste(kohta), Y))
	
	for vali in valit:
		axvali = vali
		if floor(maxX / axvali) + floor(-minX / axvali) <= 7: break
	for vali in valit:
		ayvali = vali
		if floor(maxY / ayvali) + floor(-minY / ayvali) <= 7: break
	axvali = max(axvali, xvali)
	ayvali = max(ayvali, yvali)
	if abs(float(axvali) / xvali - 2.5) < 1e-5: axvali = xvali
	if abs(float(ayvali) / yvali - 2.5) < 1e-5: ayvali = yvali
	
	X = axvali
	while X < maxX:
		piirraXKohta(X)
		X += axvali
	X = -axvali
	while X > minX:
		piirraXKohta(X)
		X -= axvali
	Y = ayvali
	while Y < maxY:
		piirraYKohta(Y)
		Y += ayvali
	Y = -ayvali
	while Y > minY:
		piirraYKohta(Y)
		Y -= ayvali
	
	# Rajaa piirto.
	rajaa(minX = minX, maxX = maxX, minY = minY, maxY = maxY)
	
	return ret

def piirraParametri(x, y, a = 0, b = 1, nimi = "", kohta = None, suunta = 0):
	"""Piirrä parametrikäyrä (x(t), y(t)), kun t käy läpi välin [a, b].
	x ja y voivat olla funktioita tai merkkijonokuvauksia t:n funktiosta.
	Esimerkiksi paraabeli välillä [-1, 1] piirretään kutsulla
	piirraKayra(lambda t: t, lambda t: t**2, -1, 1) tai
	piirraKayra("t", "t**2", -1, 1).
	'nimi' kirjoitetaan kohtaan 'kohta' suuntaan 'suunta'. Mikäli kohtaa ei
	anneta, nimi kirjoitetaan käyrän viimeiseen pisteeseen. Mikäli kohta on
	yksi luku, nimi laitetaan käyrän arvoon parametrin arvolla 'kohta'. Muuten
	käytetään arvoa 'kohta' pisteenä.
	Kuvaaja voidaan piirtää myös ilman kuvaajapohjaa."""
	
	x = funktioksi(x, "t")
	y = funktioksi(y, "t")
	
	a = float(a)
	b = float(b)
	if a >= b:
		raise ValueError("piirraKayra: alarajan on oltava pienempi kuin ylärajan.")
	
	t = a
	viim_t = a # Viimeinen sisäpuolella oleva t:n arvo.
	dt = (b - a) / 3000
	
	paksuus = "{}pt".format(tikzLuku(tila.haePaksuus()))
	vari = tila.asetukset['piirtovari']
	
	datafp = [None]
	filename = [None]
	def lopetaTiedosto():
		if datafp[0] is not None:
			datafp[0].close()
			tila.out.write("\\draw[line width={}, color={}] plot[smooth] file{{{}}};\n".format(paksuus, vari, filename[0]))
		datafp[0] = None
		filename[0] = None
	
	def aloitaTiedosto():
		if datafp[0] is None:
			tila.data_id += 1
			filename[0] = "kuva-tmp-data{}.txt".format(tila.data_id)
			datafp[0] = open(filename[0], "w")
	
	while t <= b:
		P = (x(t), y(t))
		if onkoSisapuolella(P):
			viim_t = t
			X, Y = muunna(P)
			aloitaTiedosto()
			datafp[0].write("{} {}\n".format(tikzLuku(X), tikzLuku(Y)))
		else:
			lopetaTiedosto()
		
		t += dt
	lopetaTiedosto()
	
	# Kirjoitetaan nimi.
	if kohta is None:
		kohta = (x(viim_t), y(viim_t))
	elif isinstance(kohta, int) or isinstance(kohta, float):
		kohta = (x(kohta), y(kohta))
	
	nimeaPiste(kohta, nimi, suunta)

def piirra(f, a = None, b = None, nimi = "", kohta = None, suunta = 0):
	"""Piirrä funktion f kuvaaja (f joko funktio tai x:n funktion
	merkkijonokuvaus). X-koordinaatti käy läpi välin [a, b], jos jompi kumpi
	jätetään pois, käytetään X-rajaa. Siis esimerkiksi kuvaajapohjassa ei yleensä
	erikseen tarvitse ilmoittaa väliä [a, b]. 'nimi', 'kohta' ja 'suunta'
	toimivat kuten parametrikäyrissä.
	Kuvaaja voidaan piirtää myös ilman kuvaajapohjaa."""
	
	if a is None: a = tila.asetukset['minX']
	if b is None: b = tila.asetukset['maxX']
	
	if a == float("-inf"): raise ValueError("kuvaaja: X-alaraja puuttuu.")
	if b == float("inf"): raise ValueError("kuvaaja: X-yläraja puuttuu.")
	
	f = funktioksi(f, "x")
	piirraParametri("t", f, a, b, nimi, kohta, suunta)
