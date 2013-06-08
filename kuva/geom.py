# -*- coding: UTF-8 -*-

import kuva
from kuva import *

import kuvaaja

def piste(x, y, nimi = "", suunta = 0, piirra = True):
	"""Piirtää pisteen (x, y). Nimi kirjoitetaan suuntaan 'suunta' (asteina).
	Palauttaa pisteen (x, y)."""
	
	P = (x, y)
	if piirra: kuva.piste((x, y), nimi, suunta)
	
	return P

def leikkauspiste(X, Y, nimi = "", suunta = 0, valinta = 0, piirra = True):
	"""Toimii kuten funktio piste, mutta pisteen paikka määräytyy kahdesta
	geometrisesta oliosta X ja Y (suora, jana, puolisuora, ympyrä ...). Jos
	leikkauspisteitä on useampia, 'valinta'-parametri (arvo 0, 1, ...) määrää
	mikä niistä valitaan. Samalla kuvalla valinnan pitäisi toimia aina samalla
	tavalla."""
	
	if(X["tyyppi"] == "suora" and Y["tyyppi"] == "suora"):
		x1 = float(X["A"][0])
		y1 = float(X["A"][1])
		x2 = float(X["B"][0])
		y2 = float(X["B"][1])
		u1 = float(Y["A"][0])
		v1 = float(Y["A"][1])
		u2 = float(Y["B"][0])
		v2 = float(Y["B"][1])
		
		t = (u2 * v1 - u1 * v2 + u1 * y1 + v2 * x1 - u2 * y1 - v1 * x1) / ((u2 - u1) * (y2 - y1) + (v1 - v2) * (x2 - x1))
		
		x = x1 + t * (x2 - x1)
		y = y1 + t * (y2 - y1)
	elif(X["tyyppi"] == "suora" and Y["tyyppi"] == "ympyra"):
		U = float(X["A"][0])
		V = float(X["A"][1])
		u = float(X["B"][0]) - U
		v = float(X["B"][1]) - V
		a = float(Y["keskipiste"][0])
		b = float(Y["keskipiste"][1])
		r = float(Y["sade"])
		A = u**2 + v**2
		B = 2 * u * (U - a) + 2 * v * (V - b)
		C = (U - a)**2 + (V - b)**2 - r**2
		
		diskr = B**2 - 4 * A * C
		if diskr < 0:
			diskrsqrt = 0
		elif valinta % 2 == 0:
			diskrsqrt = sqrt(diskr)
		else:
			diskrsqrt = -sqrt(diskr)
		t = (-B + diskrsqrt) / (2 * A)
		
		x = U + t * u
		y = V + t * v
	elif(X["tyyppi"] == "ympyra" and Y["tyyppi"] == "suora"):
		return leikkauspiste(Y, X, nimi, suunta, valinta, piirra)
	else:
		raise ValueError("leikauspiste: en osaa laskea näiden olioiden leikkauspistettä.")
	
	return piste(x, y, nimi, suunta, piirra)

def suora(A, B, nimi = "", kohta = 0.5, puoli = True, piirra = True, Ainf = True, Binf = True):
	"""Piirtää suoran/puolisuoran/janan joka kulkee pisteiden A ja B kautta.
	Nimi kirjoitetaan kohtaan 'kohta', missä A on kohdassa 0 ja B kohdassa 1.
	'puoli'-parametri määrää kummalle puolelle suoraa nimi merkitään. Jos parametri
	'Ainf' on true, suoran A:n puoleinen osa on rajoittamaton, vastaavasti 'Binf'.
	Palautaa suoraolion."""
	
	if(A == B): B = (B[0] + 0.01, B[1])
	
	if piirra:
		if Ainf:
			t = rajoitaLaatikkoon(B, A)
			if t == float("inf"): raise ValueError("suora: Ei voida piirtää rajoittamatonta suoraa. Rajaa kuva rajaa-funktiolla.")
			Ap = vekSumma(vekSkaalaa(B, 1 - t), vekSkaalaa(A, t))
		else:
			Ap = A
		
		if Binf:
			t = rajoitaLaatikkoon(A, B)
			if t == float("inf"): raise ValueError("suora: Ei voida piirtää rajoittamatonta suoraa. Rajaa kuva rajaa-funktiolla.")
			Bp = vekSumma(vekSkaalaa(A, 1 - t), vekSkaalaa(B, t))
		else:
			Bp = B
		
		tila.out.write("\\draw[thick] {} -- {};\n".format(tikzPiste(muunna(Ap)), tikzPiste(muunna(Bp))))
		
		suunta = 180 * atan2(-(B[1] - A[1]), B[0] - A[0]) / pi
		nimeaPiste(interpoloi(A, B, kohta), nimi, suunta + 180 * int(not puoli))
	
	return {"tyyppi": "suora", "A": A, "B": B}

def jana(A, B, nimi = "", kohta = 0.5, puoli = True, piirra = True):
	"""Vastaa funktiota suora kun Ainf = False ja Binf = False."""
	
	return suora(A, B, nimi, kohta, puoli, piirra, False, False)

def puolisuora(A, B, nimi = "", kohta = 0.5, puoli = True, piirra = True):
	"""Vastaa funktiota suora kun Ainf = False ja Binf = True."""
	
	return suora(A, B, nimi, kohta, puoli, piirra, False, True)

def ympyra(keskipiste, sade, nimi = "", kohta = 0, puoli = True, piirra = True):
	"""Piirtää ympyrän keskipisteenä 'keskipiste' ja säteenä 'sade'. Ympyrän
	nimi piirretään kohtaan 'kohta' (asteina ympyrän kaarella), 'puoli' kertoo
	kummalle puolelle. Palauttaa ympyräolion."""
	
	if(piirra):
		kuvaaja.piirraParametri(
			lambda t: keskipiste[0] + sade * cos(t), lambda t: keskipiste[1] + sade * sin(t),
			0, 2 * pi, nimi, pi * kohta / 180, kohta + 180 * int(puoli)
		)
	
	return {"tyyppi": "ympyra", "keskipiste": keskipiste, "sade": sade}

def etaisyys(A, B):
	"""Laske etäisyys pisteestä A pisteeseen B."""
	
	dx = B[0] - A[0]
	dy = B[1] - A[1]
	return sqrt(dx**2 + dy**2)

def ymparipiirrettyYmpyra(A, B, C, nimi = "", kohta = 0, puoli = True, piirra = True):
	"""Sama kuin 'ympyra', mutta ympyräksi valitaan kolmion ABC ympäripiirretty
	ympyrä."""
	
	ax = float(A[0])
	ay = float(A[1])
	bx = float(B[0])
	by = float(B[1])
	cx = float(C[0])
	cy = float(C[1])
	
	# TODO: simplify
	x = 0.5 * (
			-ay*bx*bx+bx*bx*cy-by*cy*cy+by*ay*ay+ay*cx*cx-by*by*ay
			-by*cx*cx+ax*ax*by-cy*ay*ay+by*by*cy-ax*ax*cy+cy*cy*ay
		) / (
			ax*by-ax*cy-ay*bx+ay*cx+bx*cy-by*cx
		)
	y = -0.5 * (
			-ax*bx*bx-ax*by*by+ax*cx*cx+ax*cy*cy+ax*ax*bx-ax*ax*cx
			+ay*ay*bx-ay*ay*cx-bx*cx*cx-bx*cy*cy+bx*bx*cx+by*by*cx
		) / (
			ax*by-ax*cy-ay*bx+ay*cx+bx*cy-by*cx
		)
	
	keskipiste = (x, y)
	sade = etaisyys(keskipiste, A)
	
	ympyra(keskipiste, sade, nimi, kohta, puoli, piirra)
