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

def projektio(P, s, nimi = "", suunta = 0, piirra = True):
	"""Piirtää pisteen P projektion suoralle s."""
	
	u = float(s["B"][0] - s["A"][0])
	v = float(s["B"][1] - s["A"][1])
	
	t = (u * (P[0] - s["A"][0]) + v * (P[1] - s["A"][1])) / (u**2 + v**2)
	proj = interpoloi(s["A"], s["B"], t)
	return piste(proj[0], proj[1], nimi, suunta, piirra)

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
		
		paksuus = "{}pt".format(tikzLuku(0.75 * tila.haePaksuus()))
		tila.out.write("\\draw[line width={}] {} -- {};\n".format(paksuus, tikzPiste(muunna(Ap)), tikzPiste(muunna(Bp))))
		
		suunta = 180 * atan2(B[0] - A[0], -(B[1] - A[1])) / pi
		nimeaPiste(interpoloi(A, B, kohta), nimi, suunta + 180 * int(puoli))
	
	return {"tyyppi": "suora", "A": A, "B": B}

def jana(A, B, nimi = "", kohta = 0.5, puoli = True, piirra = True):
	"""Vastaa funktiota suora kun Ainf = False ja Binf = False."""
	
	return suora(A, B, nimi, kohta, puoli, piirra, False, False)

def puolisuora(A, B, nimi = "", kohta = 0.5, puoli = True, piirra = True):
	"""Vastaa funktiota suora kun Ainf = False ja Binf = True."""
	
	return suora(A, B, nimi, kohta, puoli, piirra, False, True)

def suoraSuuntaan(A, u, v, nimi = "", kohta = 0.5, puoli = True, piirra = True):
	"""Piirtää suoran A:sta suuntaan (u, v)."""
	
	return suora(A, (A[0] + u, A[1] + v), nimi, kohta, puoli, piirra)

def puolisuoraSuuntaan(A, u, v, nimi = "", kohta = 0.5, puoli = True, piirra = True):
	"""Piirtää puolisuoran A:sta suuntaan (u, v)."""
	
	return puolisuora(A, (A[0] + u, A[1] + v), nimi, kohta, puoli, piirra)

def kaari(keskipiste, sade, alkukulma, loppukulma, nimi = "", kohta = 0, puoli = True, piirra = True):
	"""Sama kuin 'ympyra', mutta piirtää vain kaaren kulmasta 'alkukulma' kulmaan 'loppukulma'."""
	
	if(piirra):
		with paksuus(0.75):
			kuvaaja.piirraParametri(
				lambda t: keskipiste[0] + sade * cos(t), lambda t: keskipiste[1] + sade * sin(t),
				pi * alkukulma / 180, pi * loppukulma / 180, nimi, pi * kohta / 180, kohta + 180 * int(not puoli)
			)
	
	return {"tyyppi": "ympyra", "keskipiste": keskipiste, "sade": sade}

def ympyra(keskipiste, sade, nimi = "", kohta = 0, puoli = True, piirra = True):
	"""Piirtää ympyrän keskipisteenä 'keskipiste' ja säteenä 'sade'. Ympyrän
	nimi piirretään kohtaan 'kohta' (asteina ympyrän kaarella), 'puoli' kertoo
	kummalle puolelle. Palauttaa ympyräolion."""
	
	return kaari(keskipiste, sade, 0, 360, nimi, kohta, puoli, piirra)

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
	
	return ympyra(keskipiste, sade, nimi, kohta, puoli, piirra)

def ympyranKeskipiste(w, nimi = "", suunta = 0, piirra = True):
	"""Toimii kuten funktio piste, mutta valitsee pisteeksi ympyrän w keskipisteen."""
	
	return piste(w["keskipiste"][0], w["keskipiste"][1], nimi, suunta, piirra)

def ympyranKehapiste(w, kohta, nimi = "", suunta = 0, piirra = True):
	"""Piirtää ympyrän w kehäpisteen kohtaan 'kohta' asteina."""
	
	kohta = pi * kohta / 180
	sade = w["sade"]
	
	return piste(w["keskipiste"][0] + sade * cos(kohta), w["keskipiste"][1] + sade * sin(kohta), nimi, suunta, piirra)

def kulma(A, B, C, nimi = "", monista = 1, piirra = True):
	"""Piirtää kulman ABC. Kulma piirretään 'monista'-kertaisena. Palauttaa
	kulmaolion."""
	
	alkukulma = atan2(A[1] - B[1], A[0] - B[0])
	loppukulma = atan2(C[1] - B[1], C[0] - B[0])
	if(loppukulma < alkukulma): loppukulma += 2 * pi
	
	if piirra:
		Ap = muunna(A)
		Bp = muunna(B)
		Cp = muunna(C)
		alkukulmap = atan2(Ap[1] - Bp[1], Ap[0] - Bp[0])
		loppukulmap = atan2(Cp[1] - Bp[1], Cp[0] - Bp[0])
		if(loppukulmap < alkukulmap): loppukulmap += 2 * pi
		valikulmap = 0.5 * (alkukulmap + loppukulmap)
		
		kulmap = loppukulmap - alkukulmap
		sade = min(max(0.35 / kulmap, 0.5), 3)
		
		with oletusasetukset():
			paksuus(0.45)
			for i in range(monista):
				kuvaaja.piirraParametri(
					lambda t: Bp[0] + sade * cos(t), lambda t: Bp[1] + sade * sin(t),
					alkukulmap, loppukulmap, nimi, valikulmap, 180 * valikulmap / pi
				)
				nimi = ""
				sade -= 0.04
		
	
	return {"tyyppi": kulma, "alkukulma": alkukulma, "loppukulma": loppukulma}

def suorakulma(A, B, piirra = True):
	"""Piirtää suoran kulman pisteeseen B siten että oikea kylki on kohti A:tä."""
	
	if piirra:
		Ap = muunna(A)
		Bp = muunna(B)
		
		d = etaisyys(Ap, Bp)
		u = 0.3 * (Ap[0] - Bp[0]) / d
		v = 0.3 * (Ap[1] - Bp[1]) / d
		
		paksuus = "{}pt".format(tikzLuku(0.45 * tila.haePaksuus()))
		tila.out.write("\\draw[line width={}] {} -- {} -- {};\n".format(
			paksuus,
			tikzPiste(vekSumma(Bp, (u, v))),
			tikzPiste(vekSumma(Bp, (u - v, u + v))),
			tikzPiste(vekSumma(Bp, (-v, u)))
		))
	
	alkukulma = atan2(A[1] - B[1], A[0] - B[0])
	loppukulma = alkukulma + pi / 2
	return {"tyyppi": kulma, "alkukulma": alkukulma, "loppukulma": loppukulma}
