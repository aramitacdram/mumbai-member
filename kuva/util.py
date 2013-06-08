# -*- coding: UTF-8 -*-

from math import *
import tila

def funktioksi(funktio, muuttuja):
	"""Jos funktio on merkkijono, tulkitse se muuttujan funktioksi.
	Muussa tapauksessa palautetaan alkuperäinen funktio."""
	if isinstance(funktio, str):
		return eval("lambda {}: {}".format(muuttuja, funktio))
	else:
		return funktio

def tikzLuku(luku):
	"""Muotoile luku niin ettei TiKZ huuda 'Dimension too large.'"""
	return "{:.10f}".format(float(luku))

def tikzPiste(P):
	"""Muotoile piste (kahden koordinaatin tuple) oikein TiKZille."""
	X, Y = P
	
	return "({}, {})".format(tikzLuku(X), tikzLuku(Y))

def vekSumma(P, V):
	"""Laske 2D-pistetuplejen P ja V summa."""
	
	X1, Y1 = P
	X2, Y2 = V
	
	return (X1 + X2, Y1 + Y2)

def vekSkaalaa(V, c):
	"""Laske vektori V skaalattuna kertoimella c."""
	
	return (c * V[0], c * V[1])

def rajoitaLaatikkoon(A, B):
	"""Laskee puolisuoran AB leikkauspisteen rajoittavan laatikon kanssa.
	Palautusarvo on interpolaatiokerroin A:sta B:hen."""
	
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

def interpoloi(A, B, t):
	"""Laske (1-t) A + t B."""
	return vekSumma(vekSkaalaa(A, 1 - t), vekSkaalaa(B, t))
