import os

try:
	os.unlink("kuva-tmp-output.txt")
except OSError:
	pass
