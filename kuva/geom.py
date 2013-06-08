# -*- coding: UTF-8 -*-

import kuva
from kuva import *

def piste(x, y, nimi = "", suunta = (1, 0), piirra = True):
	"""Luo ja piirrä piste (x, y). Nimi kirjoitetaan suuntaan 'suunta'
	(ks kuva.nimeaPiste). Mikäli 'piirra' on False, piste jätetään piirtämättä.
	Palauttaa pisteen (x, y)."""
	
	P = (x, y)
	if piirra: kuva.piste((x, y), nimi, suunta)
	
	return P

def leikkauspiste(X, Y, nimi = "", suunta = (1, 0), piirra = True):
	"""Toimii kuten funktio piste, mutta pisteen paikka määräytyy kahdesta
	geometrisesta oliosta X ja Y (suora, jana, puolisuora, ...)."""
	
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
		
	else:
		raise ValueError("leikauspiste: en osaa laskea näiden olioiden leikkauspistettä.")
	
	return piste(x, y, nimi, suunta, piirra)

def rajoitaLaatikkoon(A, B):
	"""Laske puolisuoran AB leikkauspisteen rajoittavan laatikon kanssa kohta."""
	A = (float(A[0]), float(A[1]))
	B = (float(B[0]), float(B[1]))
	
	t = float("inf")
	if(A[0] < B[0] and tila.asetukset["maxX"] != float("inf")):
		t = min(t, (tila.asetukset["maxX"] - A[0]) / (B[0] - A[0]))
	if(A[0] > B[0] and tila.asetukset["minX"] != float("inf")):
		t = min(t, (tila.asetukset["minX"] - A[0]) / (B[0] - A[0]))
	if(A[1] < B[1] and tila.asetukset["maxY"] != float("inf")):
		t = min(t, (tila.asetukset["maxY"] - A[1]) / (B[1] - A[1]))
	if(A[1] > B[1] and tila.asetukset["minY"] != float("inf")):
		t = min(t, (tila.asetukset["minY"] - A[1]) / (B[1] - A[1]))
	
	return t

def suora(A, B, nimi = "", kohta = 0.5, puoli = True, piirra = True, Ainf = True, Binf = True):
	"""Luo ja piirtää suoran/puolisuoran/janan joka kulkee pisteiden A ja B kautta.
	Nimi kirjoitetaan kohtaan 'kohta', missä A on kohdassa 0 ja B kohdassa 1.
	'puoli'-parametri määrää kummalle puolelle suoraa nimi merkitään. Jos parametri
	'Ainf' on true, suoran A:n puoleinen osa on rajoittamaton, vastaavasti 'Binf'.
	Mikäli 'piirra' on False, suora jätetään piirtämättä. Palautaa suoraolion."""
	
	if(A == B): B = (B[0] + 0.01, B[1])
	
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
	
	return {"tyyppi": "suora", "A": A, "B": B}

def jana(A, B, nimi = "", kohta = 0.5, puoli = True, piirra = True):
	"""Vastaa funktiota suora kun Ainf = False ja Binf = False."""
	
	return suora(A, B, nimi, kohta, puoli, piirra, False, False)

def puolisuora(A, B, nimi = "", kohta = 0.5, puoli = True, piirra = True):
	"""Vastaa funktiota suora kun Ainf = False ja Binf = True."""
	
	return suora(A, B, nimi, kohta, puoli, piirra, False, True)

